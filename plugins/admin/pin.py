from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("pin") & filters.group)
async def pin_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Balas pesan yang ingin dipin.")

    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.id)
        await message.reply_text("📌 Pesan berhasil dipin.")
        logger.info(f"{message.from_user.id} pin pesan di {message.chat.id}")
        await send_log(client, message.chat.id,
            f"**PIN MESSAGE**
"
            f"👤 Admin: {message.from_user.mention} (`{message.from_user.id}`)
"
            f"📍 Grup: {message.chat.title} (`{message.chat.id}`)"
        )
    except Exception as e:
        await message.reply_text("❌ Gagal pin pesan.")
        logger.error(f"Gagal pin pesan: {e}")