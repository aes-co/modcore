from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
# from pyrogram.enums import ChatMemberStatus # Tidak perlu lagi di sini
import logging
import datetime
import time
from utils.telegram_helpers import is_admin_or_creator, send_log # UBAH

logger = logging.getLogger(__name__)

# Helper function to check if user is admin (sekarang diimpor)
# async def is_admin_or_creator(client: Client, chat_id: int, user_id: int) -> bool:
#     """Mengecek apakah pengguna adalah admin atau creator di grup."""
#     try:
#         member = await client.get_chat_member(chat_id, user_id)
#         return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
#     except Exception as e:
#         logger.error(f"Gagal mendapatkan status admin untuk user {user_id} di chat {chat_id}: {e}")
#         return False

# Helper function to get target user from command or reply
async def get_target_user(message: Message):
    """Mendapatkan target user dari argumen perintah atau dari pesan yang dibalas."""
    target_user = None
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            target_id = message.command[1]
            if target_id.isdigit():
                target_user = await message._client.get_users(int(target_id))
            elif target_id.startswith('@'):
                target_user = await message._client.get_users(target_id)
        except Exception as e:
            logger.warning(f"Gagal mendapatkan target user dari argumen: {e}")
            pass
    return target_user

# Helper function to send log to a specific channel (sekarang diimpor)
# async def send_log(app: Client, group_id: int, log_message: str):
#     """Mengirim pesan log ke channel log grup jika diatur."""
#     group_settings = app.database.get_group_settings(group_id)
#     log_channel_id = group_settings.get("log_channel_id")
#     if log_channel_id:
#         try:
#             await app.send_message(log_channel_id, log_message)
#         except Exception as e:
#             logger.error(f"Gagal mengirim log ke channel {log_channel_id} untuk grup {group_id}: {e}")

def register(app: Client):

    @app.on_message(filters.command("ban", prefixes="/") & filters.group)
    async def ban_user(client: Client, message: Message):
        logger.info(f"Ban command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = await get_target_user(message)
        if not target_user:
            await message.reply_text("Gunakan: `/ban [reply to user or user_id/username] [reason]`")
            return

        if await is_admin_or_creator(client, chat_id, target_user.id):
            await message.reply_text("❌ Tidak bisa mem-ban admin lain.")
            return

        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "Tidak ada alasan"

        try:
            await client.ban_chat_member(chat_id, target_user.id)
            await message.reply_text(f"✅ {target_user.mention} telah di-ban. Alasan: {reason}")
            logger.info(f"User {target_user.id} di-ban dari grup {chat_id} oleh {admin_id}. Alasan: {reason}")
            await send_log(app, chat_id,
                           f"**BAN**\n"
                           f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Alasan:** {reason}")
        except Exception as e:
            await message.reply_text(f"❌ Gagal mem-ban {target_user.mention}: {e}")
            logger.error(f"Gagal mem-ban user {target_user.id} di grup {chat_id}: {e}")

    @app.on_message(filters.command("kick", prefixes="/") & filters.group)
    async def kick_user(client: Client, message: Message):
        logger.info(f"Kick command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = await get_target_user(message)
        if not target_user:
            await message.reply_text("Gunakan: `/kick [reply to user or user_id/username] [reason]`")
            return

        if await is_admin_or_creator(client, chat_id, target_user.id):
            await message.reply_text("❌ Tidak bisa meng-kick admin lain.")
            return

        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "Tidak ada alasan"

        try:
            await client.kick_chat_member(chat_id, target_user.id)
            await message.reply_text(f"✅ {target_user.mention} telah di-kick. Alasan: {reason}")
            logger.info(f"User {target_user.id} di-kick dari grup {chat_id} oleh {admin_id}. Alasan: {reason}")
            await send_log(app, chat_id,
                           f"**KICK**\n"
                           f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Alasan:** {reason}")
        except Exception as e:
            await message.reply_text(f"❌ Gagal meng-kick {target_user.mention}: {e}")
            logger.error(f"Gagal meng-kick user {target_user.id} di grup {chat_id}: {e}")

    @app.on_message(filters.command("mute", prefixes="/") & filters.group)
    async def mute_user(client: Client, message: Message):
        logger.info(f"Mute command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = await get_target_user(message)
        if not target_user:
            await message.reply_text("Gunakan: `/mute [reply to user or user_id/username] [duration (e.g., 1h, 30m, 1d)] [reason]`")
            return

        if await is_admin_or_creator(client, chat_id, target_user.id):
            await message.reply_text("❌ Tidak bisa me-mute admin lain.")
            return

        duration_str = None
        reason_parts = []
        if len(message.command) > 1:
            if len(message.command) > 2 and (message.command[2].endswith(('m', 'h', 'd')) or message.command[2].isdigit()):
                duration_str = message.command[2]
                reason_parts = message.command[3:]
            else:
                reason_parts = message.command[2:]
        
        reason = " ".join(reason_parts) if reason_parts else "Tidak ada alasan"
        
        mute_until = None
        mute_duration_text = "permanen"
        if duration_str:
            try:
                num = int(duration_str[:-1])
                unit = duration_str[-1].lower()
                if unit == 'm':
                    mute_until = datetime.datetime.now() + datetime.timedelta(minutes=num)
                    mute_duration_text = f"{num} menit"
                elif unit == 'h':
                    mute_until = datetime.datetime.now() + datetime.timedelta(hours=num)
                    mute_duration_text = f"{num} jam"
                elif unit == 'd':
                    mute_until = datetime.datetime.now() + datetime.timedelta(days=num)
                    mute_duration_text = f"{num} hari"
                else:
                    await message.reply_text("❌ Format durasi tidak valid. Gunakan 'm' (menit), 'h' (jam), atau 'd' (hari). Contoh: `30m`, `1h`, `7d`.")
                    return
            except ValueError:
                reason = f"{duration_str} {reason}" if reason else duration_str
                mute_until = None
                mute_duration_text = "permanen"

        try:
            permissions = ChatPermissions(can_send_messages=False)
            until_date_timestamp = int(mute_until.timestamp()) if mute_until else 0
            await client.restrict_chat_member(chat_id, target_user.id, permissions, 
                                              until_date=until_date_timestamp)
            
            app.database.add_mute(target_user.id, chat_id, until_date_timestamp, reason)

            await message.reply_text(f"✅ {target_user.mention} telah di-mute {mute_duration_text}. Alasan: {reason}")
            logger.info(f"User {target_user.id} di-mute dari grup {chat_id} oleh {admin_id} selama {mute_duration_text}. Alasan: {reason}")
            await send_log(app, chat_id,
                           f"**MUTE**\n"
                           f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Durasi:** {mute_duration_text}\n"
                           f"**Alasan:** {reason}")
        except Exception as e:
            await message.reply_text(f"❌ Gagal me-mute {target_user.mention}: {e}")
            logger.error(f"Gagal me-mute user {target_user.id} di grup {chat_id}: {e}")

    @app.on_message(filters.command("unmute", prefixes="/") & filters.group)
    async def unmute_user(client: Client, message: Message):
        logger.info(f"Unmute command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = await get_target_user(message)
        if not target_user:
            await message.reply_text("Gunakan: `/unmute [reply to user or user_id/username]`")
            return

        try:
            permissions = ChatPermissions(can_send_messages=True,
                                          can_send_media_messages=True,
                                          can_send_other_messages=True,
                                          can_add_web_page_previews=True)
            await client.restrict_chat_member(chat_id, target_user.id, permissions)
            
            app.database.remove_mute(target_user.id, chat_id)

            await message.reply_text(f"✅ {target_user.mention} telah di-unmute.")
            logger.info(f"User {target_user.id} di-unmute dari grup {chat_id} oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**UNMUTE**\n"
                           f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)")
        except Exception as e:
            await message.reply_text(f"❌ Gagal meng-unmute {target_user.mention}: {e}")
            logger.error(f"Gagal meng-unmute user {target_user.id} di grup {chat_id}: {e}")

    @app.on_message(filters.command("warn", prefixes="/") & filters.group)
    async def warn_user(client: Client, message: Message):
        logger.info(f"Warn command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = await get_target_user(message)
        if not target_user:
            await message.reply_text("Gunakan: `/warn [reply to user or user_id/username] [reason]`")
            return

        if await is_admin_or_creator(client, chat_id, target_user.id):
            await message.reply_text("❌ Tidak bisa memperingatkan admin lain.")
            return

        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "Tidak ada alasan"

        app.database.add_warn(chat_id, target_user.id, admin_id, reason)
        warn_count = app.database.get_warn_count(chat_id, target_user.id)
        group_settings = app.database.get_group_settings(chat_id)
        warn_limit = group_settings.get("warn_limit", 3)
        warn_action = group_settings.get("warn_action", "ban")

        response_text = (
            f"⚠️ {target_user.mention} telah diperingatkan. "
            f"Jumlah peringatan: {warn_count}/{warn_limit}.\n"
            f"Alasan: {reason}"
        )
        await message.reply_text(response_text)
        logger.info(f"User {target_user.id} diperingatkan di grup {chat_id} oleh {admin_id}. Warn count: {warn_count}. Alasan: {reason}")
        await send_log(app, chat_id,
                       f"**WARN**\n"
                       f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                       f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                       f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                       f"**Jumlah Peringatan:** {warn_count}/{warn_limit}\n"
                       f"**Alasan:** {reason}")

        if warn_count >= warn_limit:
            try:
                if warn_action == "ban":
                    await client.ban_chat_member(chat_id, target_user.id)
                    action_text = "di-ban"
                elif warn_action == "mute":
                    permissions = ChatPermissions(can_send_messages=False)
                    await client.restrict_chat_member(chat_id, target_user.id, permissions, until_date=0)
                    app.database.add_mute(target_user.id, chat_id, 0, "Mute otomatis karena batas peringatan")
                    action_text = "di-mute permanen"
                elif warn_action == "kick":
                    await client.kick_chat_member(chat_id, target_user.id)
                    action_text = "di-kick"
                else:
                    action_text = "tidak ada tindakan otomatis"

                app.database.clear_warns(chat_id, target_user.id)
                await message.reply_text(f"⛔ {target_user.mention} telah mencapai batas peringatan ({warn_limit}) dan telah {action_text}.")
                logger.info(f"User {target_user.id} {action_text} otomatis karena mencapai batas peringatan di grup {chat_id}.")
                await send_log(app, chat_id,
                               f"**AUTO-ACTION ({warn_action.upper()} - WARN LIMIT)**\n"
                               f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                               f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                               f"**Alasan:** Mencapai batas peringatan ({warn_limit})")
            except Exception as e:
                await message.reply_text(f"❌ Gagal melakukan tindakan otomatis pada {target_user.mention} setelah mencapai batas peringatan: {e}")
                logger.error(f"Gagal auto-action user {target_user.id} di grup {chat_id} setelah batas peringatan: {e}")

    @app.on_message(filters.command("unwarn", prefixes="/") & filters.group)
    async def unwarn_user(client: Client, message: Message):
        logger.info(f"Unwarn command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = await get_target_user(message)
        if not target_user:
            await message.reply_text("Gunakan: `/unwarn [reply to user or user_id/username]`")
            return

        app.database.clear_warns(chat_id, target_user.id)
        await message.reply_text(f"✅ Semua peringatan untuk {target_user.mention} telah dihapus.")
        logger.info(f"Semua peringatan untuk user {target_user.id} di grup {chat_id}.")
        await send_log(app, chat_id,
                       f"**UNWARN**\n"
                       f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                       f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                       f"**Grup:** {message.chat.title} (`{chat_id}`)")

    @app.on_message(filters.command("setwarnlimit", prefixes="/") & filters.group)
    async def set_warn_limit(client: Client, message: Message):
        logger.info(f"Setwarnlimit command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_limit = group_settings.get("warn_limit", 3)
            await message.reply_text(f"Batas peringatan saat ini adalah **{current_limit}**.\n"
                                     "Gunakan: `/setwarnlimit [angka]`")
            return

        try:
            new_limit = int(message.command[1])
            if new_limit < 1:
                await message.reply_text("❌ Batas peringatan harus angka positif (minimal 1).")
                return
            app.database.update_group_setting(chat_id, "warn_limit", new_limit)
            await message.reply_text(f"✅ Batas peringatan berhasil diatur menjadi **{new_limit}**.")
            logger.info(f"Batas peringatan di grup {chat_id} diatur menjadi {new_limit} oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**SET WARN LIMIT**\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Batas Baru:** {new_limit}")
        except ValueError:
            await message.reply_text("❌ Batas peringatan harus berupa angka.")

    @app.on_message(filters.command("setwarnaction", prefixes="/") & filters.group)
    async def set_warn_action(client: Client, message: Message):
        logger.info(f"Setwarnaction command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_action = group_settings.get("warn_action", "ban")
            await message.reply_text(f"Tindakan otomatis setelah batas peringatan tercapai saat ini adalah **{current_action.upper()}**.\n"
                                     "Gunakan: `/setwarnaction [ban/mute/kick]`")
            return

        new_action = message.command[1].lower()
        if new_action not in ["ban", "mute", "kick"]:
            await message.reply_text("❌ Tindakan tidak valid. Pilihan: `ban`, `mute`, `kick`.")
            return
        
        app.database.update_group_setting(chat_id, "warn_action", new_action)
        await message.reply_text(f"✅ Tindakan otomatis setelah batas peringatan berhasil diatur menjadi **{new_action.upper()}**.")
        logger.info(f"Tindakan peringatan di grup {chat_id} diatur menjadi {new_action} oleh {admin_id}.")
        await send_log(app, chat_id,
                       f"**SET WARN ACTION**\n"
                       f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                       f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                       f"**Tindakan Baru:** {new_action.upper()}")

    @app.on_message(filters.command("setlogchannel", prefixes="/") & filters.group)
    async def set_log_channel(client: Client, message: Message):
        logger.info(f"Setlogchannel command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_log_channel = group_settings.get("log_channel_id")
            if current_log_channel:
                try:
                    channel_info = await app.get_chat(current_log_channel)
                    await message.reply_text(f"Channel log saat ini adalah **{channel_info.title}** (`{current_log_channel}`).\n"
                                             "Gunakan: `/setlogchannel [channel_id]` atau `/setlogchannel off` untuk menonaktifkan.")
                except Exception:
                    await message.reply_text(f"Channel log saat ini adalah ID **{current_log_channel}** (tidak dapat diakses).\n"
                                             "Gunakan: `/setlogchannel [channel_id]` atau `/setlogchannel off`.")
            else:
                await message.reply_text("Channel log belum diatur.\n"
                                         "Gunakan: `/setlogchannel [channel_id]` (forward pesan dari channel ke sini untuk mendapatkan ID) atau `/setlogchannel off`.")
            return

        channel_arg = message.command[1]
        if channel_arg.lower() == "off":
            app.database.update_group_setting(chat_id, "log_channel_id", None)
            await message.reply_text("✅ Channel log berhasil dinonaktifkan.")
            logger.info(f"Channel log di grup {chat_id} dinonaktifkan oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**LOG CHANNEL DISABLED**\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)")
        else:
            try:
                channel_id = int(channel_arg)
                try:
                    channel_info = await app.get_chat(channel_id)
                    if channel_info.type not in ["channel", "supergroup"]:
                        await message.reply_text("❌ ID yang diberikan bukan channel atau supergroup yang valid.")
                        return
                    app.database.update_group_setting(chat_id, "log_channel_id", channel_id)
                    await message.reply_text(f"✅ Channel log berhasil diatur ke **{channel_info.title}** (`{channel_id}`).")
                    logger.info(f"Channel log di grup {chat_id} diatur ke {channel_id} oleh {admin_id}.")
                    await send_log(app, chat_id,
                                   f"**LOG CHANNEL SET**\n"
                                   f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                                   f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                                   f"**Channel Log Baru:** {channel_info.title} (`{channel_id}`)")
                except Exception as e:
                    await message.reply_text(f"❌ Gagal memverifikasi channel ID. Pastikan bot adalah admin di channel tersebut dan ID-nya benar. Error: {e}")
                    logger.error(f"Gagal memverifikasi channel ID {channel_id} untuk grup {chat_id}: {e}")
            except ValueError:
                await message.reply_text("❌ Channel ID harus berupa angka. Forward pesan dari channel ke sini untuk mendapatkan ID-nya.")
