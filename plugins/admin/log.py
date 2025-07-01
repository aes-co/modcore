from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("log") & filters.group)
async def log_handler(_, message: Message):
    await message.reply_text("📨 Semua aksi akan tercatat di logchannel yang telah disetel.")