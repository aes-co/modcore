from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import add_watch, remove_watch, get_watchlist

watchlist = {}  # {chat_id: set(user_ids)}

@Client.on_message(filters.command("watch") & filters.reply)
async def watch_user(client: Client, message: Message):
    chat_id = message.chat.id
    admin_id = message.from_user.id
    target = message.reply_to_message.from_user

    if not target:
        return await message.reply_text("❗ Balas pesan dari user yang ingin dipantau.")

    watchlist.setdefault(chat_id, set()).add(target.id)
    await message.reply_text(f"🔍 Sekarang memantau aktivitas `{target.first_name}`.")

@Client.on_message(filters.command("unwatch") & filters.reply)
async def unwatch_user(client: Client, message: Message):
    chat_id = message.chat.id
    target = message.reply_to_message.from_user

    if not target:
        return await message.reply_text("❗ Balas pesan dari user yang ingin dilepas.")

    if chat_id in watchlist:
        watchlist[chat_id].discard(target.id)
        await message.reply_text(f"✅ Tidak lagi memantau `{target.first_name}`.")
    else:
        await message.reply_text("User tidak sedang diawasi.")

@Client.on_message(filters.command("watchlist"))
async def show_watchlist(client: Client, message: Message):
    chat_id = message.chat.id
    users = watchlist.get(chat_id, set())

    if not users:
        return await message.reply_text("📭 Tidak ada user yang dipantau.")

    text = "**👁️ Watchlist Grup Ini:**\n"
    for uid in users:
        try:
            u = await client.get_users(uid)
            text += f"• {u.mention} (`{uid}`)\n"
        except:
            text += f"• `{uid}`\n"

    await message.reply_text(text)

@Client.on_message(filters.group & filters.text)
async def watch_trigger(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id in watchlist.get(chat_id, set()):
        for admin in await client.get_chat_members(chat_id, filter="administrators"):
            try:
                await client.send_message(
                    admin.user.id,
                    f"🔔 Watchlist alert di grup: {message.chat.title}\n"
                    f"👤 {message.from_user.mention} mengirim pesan:\n\n{message.text}"
                )
            except:
                continue
