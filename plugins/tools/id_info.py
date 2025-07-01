from pyrogram import Client, filters
from pyrogram.types import Message

def register(app: Client):
    @app.on_message(filters.command("id") & filters.group)
    async def id_info_handler(client: Client, message: Message):
        user = message.from_user
        chat = message.chat
        reply = message.reply_to_message

        text = f"👤 **User ID:** `{user.id}`\n💬 **Chat ID:** `{chat.id}`"

        if reply:
            replied_user = reply.from_user
            text += f"\n📌 **Replied User ID:** `{replied_user.id}`\n📝 **Message ID:** `{reply.id}`"

        await message.reply_text(text)
