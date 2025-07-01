from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import logging

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("admins") & filters.group)
    async def list_admins(client: Client, message: Message):
        chat_id = message.chat.id
        from_user = message.from_user

        logger.info(f"/admins requested by {from_user.id} in group {chat_id}")

        try:
            members = await client.get_chat_members(chat_id, filter="administrators")
            admin_list = []
            for member in members:
                user = member.user
                if user.is_deleted:
                    name = "🪦 [Akun Terhapus]"
                elif user.username:
                    name = f"@{user.username}"
                else:
                    name = user.first_name
                status = "👑" if member.status == ChatMemberStatus.OWNER else "🔧"
                admin_list.append(f"{status} {name} (`{user.id}`)")

            if not admin_list:
                await message.reply_text("❌ Tidak ada admin ditemukan.")
                return

            text = "**👮 Daftar Admin Grup:**\n\n" + "\n".join(admin_list)
            await message.reply_text(text)
        except Exception as e:
            await message.reply_text(f"❌ Gagal mengambil daftar admin: {e}")
            logger.error(f"Gagal mengambil admin list di grup {chat_id}: {e}")
