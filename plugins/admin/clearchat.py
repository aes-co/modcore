from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("clearchat") & filters.user)
async def clearchat_handler(client: Client, message: Message):
    if not message.chat.type in ("supergroup", "group"):
        return await message.reply_text("❌ Perintah ini hanya untuk grup.")

    try:
        async for msg in client.get_chat_history(message.chat.id, limit=100):
            try:
                await client.delete_messages(message.chat.id, msg.id)
            except Exception:
                continue
        await message.reply_text("✅ Chat terakhir telah dibersihkan.")

        logger.info(f"{message.from_user.id} membersihkan chat grup {message.chat.id}")
        await send_log(client, message.chat.id,
            f"**CLEARCHAT**\n"
            f"👤 Oleh: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"📍 Grup: {message.chat.title} (`{message.chat.id}`)"
        )
    except Exception as e:
        logger.error(f"clearchat gagal di grup {message.chat.id}: {e}")
        await message.reply_text("❌ Gagal membersihkan chat.")
