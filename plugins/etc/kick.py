
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import RPCError
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_kick(app: Client):

    @app.on_message(filters.command("kick", prefixes="/") & filters.group)
    async def kick_user(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Kick command received in group {chat_id} by {admin_id}. Command: {message.text}")

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
            except RPCError as e:
                logger.warning(f"Gagal mendapatkan target user dari argumen: {e}")

        if not target_user:
            await message.reply_text("Gunakan: `/kick [reply ke user atau user_id/username] [alasan]`")
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