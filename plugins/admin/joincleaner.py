from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.new_chat_members)
async def join_cleaner_handler(client: Client, message: Message):
    chat_id = message.chat.id
    for user in message.new_chat_members:
        try:
            await client.delete_messages(chat_id, message.id)
            logger.info(f"Pesan join dari {user.id} dihapus di grup {chat_id}")
            await send_log(client, chat_id,
                f"**JOIN CLEANER**\n"
                f"👤 User: {user.mention} (`{user.id}`)\n"
                f"📍 Grup: {message.chat.title} (`{chat_id}`)\n"
                f"🗑️ Pesan join otomatis dihapus"
            )
        except Exception as e:
            logger.warning(f"Gagal hapus pesan join dari {user.id} di {chat_id}: {e}")
