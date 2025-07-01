from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("report") & filters.group)
async def report_handler(_, message: Message):
    if message.reply_to_message:
        await message.reply_text("🚨 Laporan telah dikirim ke admin!")
        logger.info(f"{message.from_user.id} melaporkan {message.reply_to_message.from_user.id} di {message.chat.id}")
    else:
        await message.reply_text("❌ Balas pesan yang ingin kamu laporkan.")