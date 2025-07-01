from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from collections import defaultdict

activity_data = defaultdict(lambda: defaultdict(int))

@Client.on_message(filters.group & filters.text)
async def track_activity(client: Client, message: Message):
    hour = datetime.now().strftime("%H")
    chat_id = message.chat.id
    activity_data[chat_id][hour] += 1

@Client.on_message(filters.command("activity") & filters.group)
async def show_activity(client: Client, message: Message):
    chat_id = message.chat.id
    data = activity_data.get(chat_id, {})
    
    if not data:
        return await message.reply_text("📭 Belum ada aktivitas yang tercatat.")

    response = "**📊 Aktivitas Grup per Jam:**\n\n"
    for hour in sorted(data):
        count = data[hour]
        response += f"`{hour}:00` — {count} pesan\n"

    await message.reply_text(response)
