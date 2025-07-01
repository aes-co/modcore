from pyrogram import Client, filters
from pyrogram.types import Message
import time

START_TIME = time.time()

def get_uptime():
    seconds = int(time.time() - START_TIME)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return f"{d} hari, {h} jam, {m} menit, {s} detik"

@Client.on_message(filters.command("uptime"))
async def uptime(client: Client, message: Message):
    await message.reply_text(f"🟢 Bot aktif selama:\n`{get_uptime()}`")
