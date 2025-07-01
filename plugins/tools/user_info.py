from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("userinfo"))
async def userinfo_handler(client: Client, message: Message):
    reply = message.reply_to_message
    user = reply.from_user if reply else message.from_user

    mention = user.mention
    username = f"@{user.username}" if user.username else "Tidak tersedia"
    full_name = user.first_name
    if user.last_name:
        full_name += f" {user.last_name}"

    text = (
        f"👤 **Informasi Pengguna**\n"
        f"📌 Nama: `{full_name}`\n"
        f"🆔 ID: `{user.id}`\n"
        f"🔗 Username: `{username}`\n"
        f"🤖 Bot?: `{user.is_bot}`"
    )
    await message.reply_text(text)

    logger.info(f"{message.from_user.id} melihat info user {user.id}")
    await send_log(client, message.chat.id,
        f"**USER INFO**\n"
        f"👤 Peminta: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"🔍 Target: {mention} (`{user.id}`)"
    )
