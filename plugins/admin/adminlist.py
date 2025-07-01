from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import send_log

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("adminlist") & filters.group)
async def adminlist_handler(client: Client, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    try:
        admins = await client.get_chat_members(chat_id, filter="administrators")
        admin_text = "**👮 Daftar Admin Grup:**\n\n"

        for admin in admins:
            user = admin.user
            name = user.mention
            if admin.status == "creator":
                admin_text += f"👑 {name} (Pemilik)\n"
            else:
                admin_text += f"• {name}\n"

        await message.reply_text(admin_text)

        logger.info(f"{message.from_user.id} meminta daftar admin di grup {chat_id}")
        await send_log(client, chat_id,
            f"**ADMIN LIST**\n"
            f"👤 Peminta: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"📌 Grup: {chat_title} (`{chat_id}`)"
        )
    except Exception as e:
        logger.error(f"Error adminlist di grup {chat_id}: {e}")
        await message.reply_text("❌ Gagal mengambil daftar admin.")
