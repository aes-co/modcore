import time
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import set_afk, get_afk, clear_afk
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("afk"))
async def afk_handler(client: Client, message: Message):
    reason = message.text.split(None, 1)[1] if len(message.command) > 1 else "Tidak ada alasan"
    await set_afk(message.from_user.id, reason)
    await message.reply_text(f"🔕 Kamu sekarang AFK.\n📄 Alasan: `{reason}`")

    logger.info(f"User {message.from_user.id} masuk mode AFK. Alasan: {reason}")
    await send_log(client, message.chat.id,
        f"**AFK Aktif**\n"
        f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"📝 Alasan: `{reason}`"
    )

@Client.on_message(filters.private | filters.group)
async def check_afk(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        afk = await get_afk(target_id)
        if afk:
            await message.reply_text(f"💤 User ini sedang AFK.\n📄 Alasan: `{afk['reason']}`")

    if message.from_user:
        if await get_afk(message.from_user.id):
            await clear_afk(message.from_user.id)
            await message.reply_text("✅ Welcome back! Status AFK kamu sudah dihapus.")

            logger.info(f"User {message.from_user.id} kembali dari AFK.")
            await send_log(client, message.chat.id,
                f"**AFK Selesai**\n"
                f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)"
            )
