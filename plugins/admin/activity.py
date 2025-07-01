from pyrogram import Client, filters
from pyrogram.types import Message
import time
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

last_seen = {}

@Client.on_message(filters.group)
async def track_activity(_, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    timestamp = int(time.time())

    if chat_id not in last_seen:
        last_seen[chat_id] = {}

    last_seen[chat_id][user_id] = timestamp

@Client.on_message(filters.command("seen") & filters.group)
async def seen_handler(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Balas pesan pengguna yang ingin kamu cek terakhir aktifnya.")

    target = message.reply_to_message.from_user
    chat_id = message.chat.id

    if chat_id in last_seen and target.id in last_seen[chat_id]:
        ts = last_seen[chat_id][target.id]
        delta = int(time.time()) - ts

        days, rem = divmod(delta, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        uptime = f"{days}d {hours}h {minutes}m {seconds}s"

        await message.reply_text(f"👀 {target.mention} terakhir terlihat:\n`{uptime} yang lalu`")
    else:
        await message.reply_text("ℹ️ Tidak ada data aktivitas user tersebut.")

    logger.info(f"{message.from_user.id} melihat aktivitas user {target.id}")
    await send_log(_, chat_id,
        f"**SEEN CHECK**\n"
        f"👤 Peminta: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"👀 Target: {target.mention} (`{target.id}`)"
    )
