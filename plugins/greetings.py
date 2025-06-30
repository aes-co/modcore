from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# from pyrogram.enums import ChatMemberStatus # Tidak perlu lagi di sini
import logging
import json
from plugins.ai_handler import generate_creative_message_ai
from utils.telegram_helpers import is_admin_or_creator # UBAH

logger = logging.getLogger(__name__)

# Helper function to check if user is admin or creator (sekarang diimpor)
# async def is_admin_or_creator(client: Client, chat_id: int, user_id: int) -> bool:
#     """Mengecek apakah pengguna adalah admin atau creator di grup."""
#     try:
#         member = await client.get_chat_member(chat_id, user_id)
#         return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
#     except Exception as e:
#         logger.error(f"Gagal mendapatkan status admin untuk user {user_id} di chat {chat_id}: {e}")
#         return False

def register(app: Client):

    @app.on_message(filters.new_chat_members & filters.group)
    async def welcome_message_handler(client: Client, message: Message):
        logger.info(f"New chat members detected in group {message.chat.id}. Members: {[u.id for u in message.new_chat_members]}")
        chat_id = message.chat.id
        group_settings = app.database.get_group_settings(chat_id)
        
        welcome_message_text = group_settings.get("welcome_message")
        welcome_button_data = group_settings.get("welcome_button_data")

        if not welcome_message_text:
            return

        for user in message.new_chat_members:
            if user.is_bot:
                continue

            final_message = welcome_message_text.replace("{user}", user.mention)
            final_message = final_message.replace("{chat_title}", message.chat.title)
            final_message = final_message.replace("{chat_id}", str(chat_id))
            final_message = final_message.replace("{first_name}", user.first_name)
            final_message = final_message.replace("{last_name}", user.last_name if user.last_name else "")
            final_message = final_message.replace("{username}", f"@{user.username}" if user.username else user.first_name)

            reply_markup = None
            if welcome_button_data:
                try:
                    button_list = json.loads(welcome_button_data)
                    keyboard_buttons = []
                    for btn in button_list:
                        if "text" in btn and "url" in btn:
                            keyboard_buttons.append(InlineKeyboardButton(btn["text"], url=btn["url"]))
                    if keyboard_buttons:
                        reply_markup = InlineKeyboardMarkup([keyboard_buttons])
                except json.JSONDecodeError:
                    logger.error(f"Gagal parse JSON tombol selamat datang di grup {chat_id}: {welcome_button_data}")
            
            try:
                await message.reply_text(final_message, reply_markup=reply_markup, disable_web_page_preview=True)
                logger.info(f"Pesan selamat datang dikirim untuk {user.id} di grup {chat_id}.")
            except Exception as e:
                logger.error(f"Gagal mengirim pesan selamat datang untuk {user.id} di grup {chat_id}: {e}")

    @app.on_message(filters.left_chat_member & filters.group)
    async def goodbye_message_handler(client: Client, message: Message):
        logger.info(f"Left chat member detected in group {message.chat.id}. Member: {message.left_chat_member.id if message.left_chat_member else 'N/A'}")
        chat_id = message.chat.id
        group_settings = app.database.get_group_settings(chat_id)
        
        goodbye_message_text = group_settings.get("goodbye_message")

        if not goodbye_message_text:
            return

        user = message.left_chat_member
        if user.id == client.me.id:
            logger.info(f"Bot meninggalkan grup {chat_id}.")
            return

        final_message = goodbye_message_text.replace("{user}", user.mention)
        final_message = final_message.replace("{chat_title}", message.chat.title)
        final_message = final_message.replace("{chat_id}", str(chat_id))
        final_message = final_message.replace("{first_name}", user.first_name)
        final_message = final_message.replace("{last_name}", user.last_name if user.last_name else "")
        final_message = final_message.replace("{username}", f"@{user.username}" if user.username else user.first_name)
        
        try:
            await message.reply_text(final_message, disable_web_page_preview=True)
            logger.info(f"Pesan selamat tinggal dikirim untuk {user.id} di grup {chat_id}.")
        except Exception as e:
            logger.error(f"Gagal mengirim pesan selamat tinggal untuk {user.id} di grup {chat_id}: {e}")

    @app.on_message(filters.command("setwelcome", prefixes="/") & filters.group)
    async def set_welcome_message(client: Client, message: Message):
        logger.info(f"Setwelcome command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_welcome = group_settings.get("welcome_message")
            await message.reply_text(
                "Gunakan: `/setwelcome [pesan]` untuk mengatur pesan selamat datang.\n"
                "Gunakan `/setwelcome off` untuk menonaktifkan.\n\n"
                "**Placeholder yang tersedia:**\n"
                "`{user}`: Mention pengguna baru\n"
                "`{chat_title}`: Nama grup\n"
                "`{chat_id}`: ID grup\n"
                "`{first_name}`: Nama depan pengguna\n"
                "`{last_name}`: Nama belakang pengguna\n"
                "`{username}`: Username pengguna (jika ada)\n\n"
                f"**Pesan saat ini:**\n`{current_welcome}`" if current_welcome else "**Belum diatur.**"
            )
            return

        new_message = " ".join(message.command[1:])
        if new_message.lower() == "off":
            app.database.update_group_setting(chat_id, "welcome_message", None)
            app.database.update_group_setting(chat_id, "welcome_button_data", None)
            await message.reply_text("✅ Pesan selamat datang berhasil dinonaktifkan.")
            logger.info(f"Pesan selamat datang di grup {chat_id} dinonaktifkan oleh {admin_id}.")
        else:
            app.database.update_group_setting(chat_id, "welcome_message", new_message)
            await message.reply_text("✅ Pesan selamat datang berhasil diatur.")
            logger.info(f"Pesan selamat datang di grup {chat_id} diatur oleh {admin_id}.")

    @app.on_message(filters.command("setgoodbye", prefixes="/") & filters.group)
    async def set_goodbye_message(client: Client, message: Message):
        logger.info(f"Setgoodbye command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_goodbye = group_settings.get("goodbye_message")
            await message.reply_text(
                "Gunakan: `/setgoodbye [pesan]` untuk mengatur pesan selamat tinggal.\n"
                "Gunakan `/setgoodbye off` untuk menonaktifkan.\n\n"
                "**Placeholder yang tersedia:**\n"
                "`{user}`: Mention pengguna yang keluar\n"
                "`{chat_title}`: Nama grup\n"
                "`{chat_id}`: ID grup\n"
                "`{first_name}`: Nama depan pengguna\n"
                "`{last_name}`: Nama belakang pengguna\n"
                "`{username}`: Username pengguna (jika ada)\n\n"
                f"**Pesan saat ini:**\n`{current_goodbye}`" if current_goodbye else "**Belum diatur.**"
            )
            return

        new_message = " ".join(message.command[1:])
        if new_message.lower() == "off":
            app.database.update_group_setting(chat_id, "goodbye_message", None)
            await message.reply_text("✅ Pesan selamat tinggal berhasil dinonaktifkan.")
            logger.info(f"Pesan selamat tinggal di grup {chat_id} dinonaktifkan oleh {admin_id}.")
        else:
            app.database.update_group_setting(chat_id, "goodbye_message", new_message)
            await message.reply_text("✅ Pesan selamat tinggal berhasil diatur.")
            logger.info(f"Pesan selamat tinggal di grup {chat_id} diatur oleh {admin_id}.")

    @app.on_message(filters.command("setwelcomebutton", prefixes="/") & filters.group)
    async def set_welcome_button(client: Client, message: Message):
        logger.info(f"Setwelcomebutton command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_button_data = group_settings.get("welcome_button_data")
            button_info = ""
            if current_button_data:
                try:
                    btn = json.loads(current_button_data)[0]
                    button_info = f"\n**Tombol saat ini:** `{btn['text']}` -> `{btn['url']}`"
                except Exception:
                    button_info = "\n**Tombol saat ini:** (Error parsing data)"

            await message.reply_text(
                "Gunakan: `/setwelcomebutton [Teks Tombol] | [URL]` untuk menambahkan tombol ke pesan selamat datang.\n"
                "Gunakan `/setwelcomebutton off` untuk menghapus tombol.\n\n"
                "**Contoh:** `/setwelcomebutton Kunjungi Website Kami | https://example.com`"
                f"{button_info}"
            )
            return

        button_arg = " ".join(message.command[1:])
        if button_arg.lower() == "off":
            app.database.update_group_setting(chat_id, "welcome_button_data", None)
            await message.reply_text("✅ Tombol selamat datang berhasil dihapus.")
            logger.info(f"Tombol selamat datang di grup {chat_id} dihapus oleh {admin_id}.")
        else:
            parts = button_arg.split('|', 1)
            if len(parts) == 2:
                button_text = parts[0].strip()
                button_url = parts[1].strip()
                if not button_text or not button_url:
                    await message.reply_text("❌ Format tidak valid. Teks tombol dan URL tidak boleh kosong.")
                    return
                
                button_data = json.dumps([{"text": button_text, "url": button_url}])
                app.database.update_group_setting(chat_id, "welcome_button_data", button_data)
                await message.reply_text(f"✅ Tombol selamat datang berhasil diatur:\n"
                                         f"Teks: `{button_text}`\nURL: `{button_url}`")
                logger.info(f"Tombol selamat datang di grup {chat_id} diatur oleh {admin_id}.")
            else:
                await message.reply_text("❌ Format tidak valid. Gunakan: `/setwelcomebutton [Teks Tombol] | [URL]`")

    @app.on_message(filters.command("generatewelcome", prefixes="/") & filters.group)
    async def generate_welcome_message_ai_command(client: Client, message: Message):
        if not getattr(app, "use_ai", False):
            await message.reply("❌ Fitur AI tidak aktif.")
            return
        
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        theme = " ".join(message.command[1:])
        if not theme:
            theme = "pesan selamat datang umum untuk grup Telegram"

        await message.reply("⏳ Sedang membuat pesan selamat datang dengan AI...")
        try:
            generated_message = await generate_creative_message_ai(
                f"pesan selamat datang untuk grup Telegram dengan tema: {theme}",
                app.ai_provider,
                app.ollama_model
            )
            await message.reply(
                f"✨ **Pesan Selamat Datang AI:**\n\n"
                f"{generated_message}\n\n"
                f"Anda bisa mengaturnya dengan `/setwelcome [pesan ini]`"
            )
            logger.info(f"Pesan selamat datang AI dihasilkan untuk grup {chat_id} dengan tema: {theme}.")
        except Exception as e:
            await message.reply(f"❌ Gagal membuat pesan selamat datang dengan AI: {e}")
            logger.error(f"Gagal membuat pesan selamat datang AI untuk grup {chat_id}: {e}")

    @app.on_message(filters.command("generategoodbye", prefixes="/") & filters.group)
    async def generate_goodbye_message_ai_command(client: Client, message: Message):
        if not getattr(app, "use_ai", False):
            await message.reply("❌ Fitur AI tidak aktif.")
            return

        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        theme = " ".join(message.command[1:])
        if not theme:
            theme = "pesan selamat tinggal umum untuk grup Telegram"

        await message.reply("⏳ Sedang membuat pesan selamat tinggal dengan AI...")
        try:
            generated_message = await generate_creative_message_ai(
                f"pesan selamat tinggal untuk grup Telegram dengan tema: {theme}",
                app.ai_provider,
                app.ollama_model
            )
            await message.reply(
                f"✨ **Pesan Selamat Tinggal AI:**\n\n"
                f"{generated_message}\n\n"
                f"Anda bisa mengaturnya dengan `/setgoodbye [pesan ini]`"
            )
            logger.info(f"Pesan selamat tinggal AI dihasilkan untuk grup {chat_id} dengan tema: {theme}.")
        except Exception as e:
            await message.reply(f"❌ Gagal membuat pesan selamat tinggal dengan AI: {e}")
            logger.error(f"Gagal membuat pesan selamat tinggal AI untuk grup {chat_id}: {e}")
