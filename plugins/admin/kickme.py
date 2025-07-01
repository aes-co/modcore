from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("kickme") & filters.group)
async def kick_me(client: Client, message: Message):
    try:
        await message.reply_text("👋 Selamat tinggal...")
        await client.kick_chat_member(message.chat.id, message.from_user.id)
        await client.unban_chat_member(message.chat.id, message.from_user.id)  # Agar bisa join lagi
    except Exception as e:
        await message.reply_text("❌ Gagal mengeluarkan kamu. Apakah aku punya izin yang cukup?")
