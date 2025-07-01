from pyrogram import Client, filters
from pyrogram.types import Message
from collections import defaultdict
from datetime import datetime

activity_count = defaultdict(int)
user_activity = defaultdict(lambda: defaultdict(int))  # {chat_id: {user_id: count}}

@Client.on_message(filters.group & filters.text)
async def count_insight(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    hour = datetime.now().strftime("%H")

    activity_count[(chat_id, hour)] += 1
    user_activity[chat_id][user_id] += 1

@Client.on_message(filters.command("insight") & filters.group)
async def show_insight(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        chat = await client.get_chat(chat_id)
        member_count = chat.members_count
    except:
        member_count = "?"

    # top user
    activity = user_activity.get(chat_id, {})
    if activity:
        top_id = max(activity, key=activity.get)
        top_count = activity[top_id]
        try:
            top_user = await client.get_users(top_id)
            top_name = top_user.mention
        except:
            top_name = f"`{top_id}`"
    else:
        top_name = "Belum ada"
        top_count = 0

    # jam sibuk
    jam_data = {
        hour: activity_count.get((chat_id, hour), 0)
        for hour in [f"{i:02d}" for i in range(24)]
    }
    busiest = max(jam_data, key=jam_data.get) if any(jam_data.values()) else "-"

    await message.reply_text(
        f"📈 **Insight Grup**\n"
        f"👥 Total Member: `{member_count}`\n"
        f"🔥 User Teraktif: {top_name} (`{top_count}` pesan)\n"
        f"🕓 Jam Tersibuk: `{busiest}:00`\n"
    )
