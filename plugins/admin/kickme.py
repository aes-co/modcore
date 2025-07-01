from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import send_log

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("kickme") & filters.group)
async def kickme_handler(client: Client, message: Message):
    user = message.from_user
    chat = message.chat

    try:
        await client.kick_chat_member(chat.id, user.id)
        await client.unban_chat_member(chat.id, user.id)
        await message.reply_text("👋 Selamat tinggal!")

        logger.info(f"{user.id} menggunakan /kickme di {chat.id}")
        await send_log(client, chat.id,
            f"**KICKME**
"
            f"👤 User: {user.mention} (`{user.id}`)
"
            f"📍 Grup: {chat.title} (`{chat.id}`)
"
            f"✌️ Keluar dengan sukarela."
        )
    except Exception as e:
        await message.reply_text("❌ Gagal mengeluarkanmu dari grup.")
        logger.error(f"Kickme gagal untuk {user.id} di {chat.id}: {e}")