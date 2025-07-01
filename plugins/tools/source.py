from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

SOURCE_URL = "https://github.com/aeswnh/modcore"

@Client.on_message(filters.command("source"))
async def source_handler(client: Client, message: Message):
    await message.reply_text(f"📦 Source code bot ini tersedia di GitHub:\n🔗 {SOURCE_URL}")

    logger.info(f"{message.from_user.id} membuka tautan source code")
    await send_log(client, message.chat.id,
        f"**SOURCE LINK**\n"
        f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)"
    )
