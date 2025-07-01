from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("purge") & filters.group)
async def purge_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Balas pesan awal yang ingin dihapus.")

    start_msg_id = message.reply_to_message.id
    end_msg_id = message.id

    deleted = 0
    for msg_id in range(start_msg_id, end_msg_id):
        try:
            await client.delete_messages(message.chat.id, msg_id)
            deleted += 1
        except:
            continue

    await message.reply_text(f"✅ {deleted} pesan berhasil dihapus.")
    logger.info(f"{message.from_user.id} purge {deleted} pesan di grup {message.chat.id}")
    await send_log(client, message.chat.id,
        f"**PURGE**
"
        f"👤 Admin: {message.from_user.mention} (`{message.from_user.id}`)
"
        f"📍 Grup: {message.chat.title} (`{message.chat.id}`)
"
        f"🧹 Jumlah: {deleted} pesan"
    )