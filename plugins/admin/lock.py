from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("lock") & filters.group)
async def lock_handler(client: Client, message: Message):
    try:
        await client.set_chat_permissions(message.chat.id, ChatPermissions())
        await message.reply_text("🔒 Semua pesan telah dikunci untuk non-admin.")
        logger.info(f"{message.from_user.id} mengunci grup {message.chat.id}")
        await send_log(client, message.chat.id,
            f"**LOCK CHAT**
"
            f"👤 Admin: {message.from_user.mention} (`{message.from_user.id}`)
"
            f"📍 Grup: {message.chat.title} (`{message.chat.id}`)"
        )
    except Exception as e:
        logger.error(f"Gagal lock chat: {e}")
        await message.reply_text("❌ Gagal mengunci pesan.")