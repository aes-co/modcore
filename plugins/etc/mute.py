
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging
import datetime

logger = logging.getLogger(__name__)

def register_mute(app: Client):

    @app.on_message(filters.command("mute", prefixes="/") & filters.group)
    async def mute_user(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Mute command received in group {chat_id} by {admin_id}. Command: {message.text}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = None
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            try:
                identifier = message.command[1]
                if identifier.isdigit():
                    target_user = await client.get_users(int(identifier))
                elif identifier.startswith("@"):
                    target_user = await client.get_users(identifier)
            except Exception as e:
                logger.warning(f"Gagal mendapatkan target user dari argumen: {e}")

        if not target_user:
            await message.reply_text("Gunakan: `/mute [reply ke user atau user_id/username] [durasi (e.g., 30m, 2h)] [alasan]`")
            return

        if await is_admin_or_creator(client, chat_id, target_user.id):
            await message.reply_text("❌ Tidak bisa me-mute admin lain.")
            return

        duration_str = None
        reason_parts = []

        if len(message.command) > 2:
            if message.command[2].endswith(('m', 'h', 'd')) or message.command[2].isdigit():
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
                    await message.reply_text("❌ Format durasi tidak valid. Gunakan: `30m`, `2h`, `1d`, dll.")
                    return
            except ValueError:
                reason = f"{duration_str} {reason}" if reason else duration_str
                mute_until = None
                mute_duration_text = "permanen"

        try:
            permissions = ChatPermissions(can_send_messages=False)
            until_timestamp = int(mute_until.timestamp()) if mute_until else 0
            await client.restrict_chat_member(chat_id, target_user.id, permissions, until_date=until_timestamp)

            app.database.add_mute(target_user.id, chat_id, until_timestamp, reason)

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