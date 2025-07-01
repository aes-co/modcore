from pyrogram import Client, filters
from pyrogram.types import Message
import re
import logging

logger = logging.getLogger(__name__)

link_regex = re.compile(r"(https?://\S+|t\.me/\S+|telegram\.me/\S+)", re.IGNORECASE)

def register(app: Client):

    @app.on_message(filters.group & filters.text & ~filters.service)
    async def detect_link(client: Client, message: Message):
        if not message.from_user or message.from_user.is_bot:
            return

        if not link_regex.search(message.text):
            return

        chat_id = message.chat.id
        user_id = message.from_user.id

        # Admin skip check
        try:
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in ("administrator", "creator"):
                return
        except Exception:
            return  # Jika gagal cek, skip saja

        try:
            await message.delete()
            logger.info(f"Pesan berisi link dari {user_id} dihapus dari grup {chat_id}")
            await message.reply_text(
                f"⚠️ {message.from_user.mention}, tautan tidak diizinkan di grup ini.",
                quote=True
            )
        except Exception as e:
            logger.error(f"Gagal menghapus pesan link dari {user_id} di grup {chat_id}: {e}")
