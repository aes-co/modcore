from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import is_admin_or_creator

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("clearchat") & filters.group)
    async def clear_chat(client: Client, message: Message):
        chat_id = message.chat.id
        sender_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, sender_id):
            await message.reply_text("❌ Perintah ini hanya bisa digunakan oleh admin.")
            return

        count = 100  # default
        if len(message.command) > 1 and message.command[1].isdigit():
            count = min(int(message.command[1]), 300)

        try:
            await message.reply_text(f"🧹 Menghapus {count} pesan terakhir...")
            async for msg in client.get_chat_history(chat_id, limit=count):
                try:
                    await client.delete_messages(chat_id, msg.id)
                except Exception:
                    continue

            logger.info(f"{count} pesan dihapus di grup {chat_id} oleh admin {sender_id}")
        except Exception as e:
            await message.reply_text(f"❌ Gagal menghapus pesan: {e}")
            logger.error(f"Gagal menghapus pesan di grup {chat_id}: {e}")
