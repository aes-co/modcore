from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import logging
import time
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.text & filters.group & ~filters.via_bot)
    async def flood_spam_detector(client: Client, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        # --- DEBUG START ---
        is_user_admin = await is_admin_or_creator(client, chat_id, user_id)
        logger.info(f"DEBUG: User {user_id} (sender) is_admin_or_creator: {is_user_admin} in chat {chat_id} for antiflood.")
        # --- DEBUG END ---

        if is_user_admin: # Admin tidak terpengaruh antiflood
            return

        group_settings = app.database.get_group_settings(chat_id)
        flood_limit = group_settings.get("flood_limit", 10)
        flood_time_window = group_settings.get("flood_time_window", 5)
        spam_detection_enabled = group_settings.get("spam_detection_enabled", False)

        current_time = int(time.time())
        user_flood_data = app.database.get_flood_data(user_id, chat_id)
        
        message_count = user_flood_data["message_count"]
        last_message_time = user_flood_data["last_message_time"]

        if current_time - last_message_time > flood_time_window:
            message_count = 1
        else:
            message_count += 1
        
        app.database.update_flood_data(user_id, chat_id, message_count, current_time)

        if message_count >= flood_limit:
            try:
                await message.delete()
                permissions = ChatPermissions(can_send_messages=False)
                await client.restrict_chat_member(chat_id, user_id, permissions, until_date=current_time + 60)
                app.database.add_mute(user_id, chat_id, current_time + 60, "Mute otomatis karena flood")
                app.database.clear_flood_data(user_id, chat_id)
                
                await message.reply_text(
                    f"🚫 {message.from_user.mention} terdeteksi melakukan flood dan di-mute selama 60 detik."
                )
                logger.info(f"User {user_id} di-mute karena flood di grup {chat_id}.")
                await send_log(app, chat_id,
                               f"**AUTO-MUTE (FLOOD)**\n"
                               f"**User:** {message.from_user.mention} (`{user_id}`)\n"
                               f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                               f"**Alasan:** Terdeteksi flood ({flood_limit} pesan dalam {flood_time_window} detik).")
            except Exception as e:
                logger.error(f"Gagal menindak flood dari user {user_id} di {chat_id}: {e}")

        if spam_detection_enabled and message.text and message_count > 2:
            # Logika deteksi spam yang lebih canggih bisa ditambahkan di sini
            pass

    @app.on_message(filters.command("setfloodlimit", prefixes="/") & filters.group)
    async def set_flood_limit_command(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        # --- DEBUG START ---
        is_user_admin = await is_admin_or_creator(client, chat_id, admin_id)
        logger.info(f"DEBUG: User {admin_id} (sender) is_admin_or_creator: {is_user_admin} in chat {chat_id} for setfloodlimit.")
        # --- DEBUG END ---

        if not is_user_admin:
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 3:
            group_settings = app.database.get_group_settings(chat_id)
            current_limit = group_settings.get("flood_limit", 10)
            current_window = group_settings.get("flood_time_window", 5)
            await message.reply_text(
                f"Batas flood saat ini: **{current_limit}** pesan dalam **{current_window}** detik.\n"
                "Gunakan: `/setfloodlimit [jumlah_pesan] [jendela_waktu_detik]`"
            )
            return

        try:
            new_limit = int(message.command[1])
            new_window = int(message.command[2])
            if new_limit < 1 or new_window < 1:
                await message.reply_text("❌ Jumlah pesan dan jendela waktu harus angka positif.")
                return
            
            app.database.update_group_setting(chat_id, "flood_limit", new_limit)
            app.database.update_group_setting(chat_id, "flood_time_window", new_window)
            await message.reply_text(f"✅ Batas flood berhasil diatur menjadi **{new_limit}** pesan dalam **{new_window}** detik.")
            logger.info(f"Batas flood di grup {chat_id} diatur menjadi {new_limit}/{new_window} oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**SET FLOOD LIMIT**\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Batas Baru:** {new_limit} pesan dalam {new_window} detik.")
        except ValueError:
            await message.reply_text("❌ Jumlah pesan dan jendela waktu harus berupa angka.")

    @app.on_message(filters.command("setspamdetection", prefixes="/") & filters.group)
    async def set_spam_detection_command(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        # --- DEBUG START ---
        is_user_admin = await is_admin_or_creator(client, chat_id, admin_id)
        logger.info(f"DEBUG: User {admin_id} (sender) is_admin_or_creator: {is_user_admin} in chat {chat_id} for setspamdetection.")
        # --- DEBUG END ---

        if not is_user_admin:
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            status = "aktif" if group_settings["spam_detection_enabled"] else "tidak aktif"
            await message.reply_text(f"Deteksi spam saat ini **{status}**.\n"
                                     "Gunakan `/setspamdetection on` atau `/setspamdetection off`.")
            return

        action = message.command[1].lower()
        if action == "on":
            app.database.update_group_setting(chat_id, "spam_detection_enabled", True)
            await message.reply_text("✅ Deteksi spam berhasil diaktifkan.")
            logger.info(f"Deteksi spam diaktifkan di grup {chat_id} oleh admin {admin_id}.")
        elif action == "off":
            app.database.update_group_setting(chat_id, "spam_detection_enabled", False)
            await message.reply_text("✅ Deteksi spam berhasil dinonaktifkan.")
            logger.info(f"Deteksi spam dinonaktifkan di grup {chat_id} oleh admin {admin_id}.")
        else:
            await message.reply_text("❌ Perintah tidak valid. Gunakan `/setspamdetection on` atau `/setspamdetection off`.")
