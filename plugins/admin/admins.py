from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import logging
from utils.telegram_helpers import is_admin_or_creator

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("admins") & filters.group)
    async def list_admins(client: Client, message: Message):
        chat_id = message.chat.id
        sender_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, sender_id):
            await message.reply_text("❌ Hanya admin grup yang bisa menggunakan perintah ini.")
            return

        try:
            admins = await client.get_chat_members(chat_id, filter="administrators")
            text = f"📋 **Daftar Admin di {message.chat.title}:**\n\n"
            for admin in admins:
                user = admin.user
                status = "👑 Owner" if admin.status == ChatMemberStatus.OWNER else "🔧 Admin"
                text += f"- {user.mention} `{user.id}` [{status}]\n"

            await message.reply_text(text)
            logger.info(f"Daftar admin diminta oleh {sender_id} di grup {chat_id}")
        except Exception as e:
            await message.reply_text(f"❌ Gagal mengambil daftar admin: {e}")
            logger.error(f"Gagal mengambil daftar admin di grup {chat_id}: {e}")
