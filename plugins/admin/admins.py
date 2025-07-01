from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("admins") & filters.group)
async def admins_handler(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        admins = await client.get_chat_members(chat_id, filter="administrators")
        text = "**👮 Admins Grup Ini:**\n\n"
        for admin in admins:
            user = admin.user
            status = "👑" if admin.status == "creator" else "•"
            text += f"{status} {user.mention}\n"
        await message.reply_text(text)

        logger.info(f"{message.from_user.id} melihat daftar admin grup {chat_id}")
        await send_log(client, chat_id,
            f"**ADMINS CMD**\n"
            f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"📍 Grup: `{chat_id}`"
        )
    except Exception as e:
        logger.error(f"Gagal mengambil admin grup {chat_id}: {e}")
        await message.reply_text("❌ Tidak bisa mengambil daftar admin.")
