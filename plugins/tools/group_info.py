from pyrogram import Client, filters
from pyrogram.types import Message

def register(app: Client):
    @app.on_message(filters.command("groupinfo") & filters.group)
    async def group_info_handler(client: Client, message: Message):
        chat = message.chat
        try:
            members_count = await client.get_chat_members_count(chat.id)
            bot_member = await client.get_chat_member(chat.id, client.me.id)

            info_text = (
                f"👥 **Group Info**\n"
                f"• **Nama:** {chat.title}\n"
                f"• **ID:** `{chat.id}`\n"
                f"• **Tipe:** {chat.type.name.capitalize()}\n"
                f"• **Anggota:** {members_count}\n"
                f"• **Status Bot:** {bot_member.status.name.capitalize()}"
            )
            await message.reply_text(info_text)
        except Exception as e:
            await message.reply_text(f"❌ Gagal mengambil info grup: {e}")
