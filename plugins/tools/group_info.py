from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("groupinfo") & filters.group)
async def group_info_handler(client: Client, message: Message):
    chat = message.chat
    text = (
        f"**ℹ️ Informasi Grup**\n"
        f"📌 Nama: {chat.title}\n"
        f"🆔 ID: `{chat.id}`\n"
        f"👥 Tipe: `{chat.type}`\n"
        f"🧾 Username: @{chat.username if chat.username else 'Tidak ada'}\n"
        f"👮‍♂️ Admin: {message.from_user.mention}"
    )
    await message.reply_text(text)

    logger.info(f"{message.from_user.id} meminta info grup {chat.id}")
    await send_log(client, chat.id,
        f"**GROUP INFO**\n"
        f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"📌 Grup: {chat.title} (`{chat.id}`)"
    )
