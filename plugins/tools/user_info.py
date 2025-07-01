from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import is_admin_or_creator

def register(app: Client):
    @app.on_message(filters.command("userinfo") & filters.group)
    async def user_info_handler(client: Client, message: Message):
        chat_id = message.chat.id
        sender_id = message.from_user.id

        # Check admin
        if not await is_admin_or_creator(client, chat_id, sender_id):
            await message.reply_text("❌ Hanya admin yang dapat menggunakan perintah ini.")
            return

        # Target user
        target = message.reply_to_message.from_user if message.reply_to_message else message.from_user

        info_text = (
            f"👤 **User Info**\n"
            f"• **Nama:** {target.first_name or '-'}\n"
            f"• **Username:** @{target.username if target.username else '-'}\n"
            f"• **ID:** `{target.id}`\n"
            f"• **Bot:** {'Ya' if target.is_bot else 'Tidak'}\n"
            f"• **Bahasa:** `{target.language_code or 'unknown'}`"
        )

        await message.reply_text(info_text)
