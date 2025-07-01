from pyrogram import Client, filters
from pyrogram.types import Message
import logging

from utils.telegram_helpers import is_admin_or_creator, send_log
from plugins.etc.helpers import get_target_user

logger = logging.getLogger(__name__)

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
