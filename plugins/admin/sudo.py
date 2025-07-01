from pyrogram import Client, filters
from pyrogram.types import Message

SUDO_USERS = {123456789, 987654321}

@Client.on_message(filters.command(["addsudo", "rmsudo"]) & filters.user(SUDO_USERS))
async def sudo_handler(_, message: Message):
    await message.reply_text("✅ Fitur sudo ditangani backend (MongoDB), akan diterapkan terintegrasi.")