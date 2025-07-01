
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_unmute(app: Client):

    @app.on_message(filters.command("unmute", prefixes="/") & filters.group)
    async def unmute_user(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Unmute command received in group {chat_id} by {admin_id}. Command: {message.text}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        target_user = None
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            try:
                identifier = message.command[1]
                if identifier.isdigit():
                    target_user = await client.get_users(int(identifier))
                elif identifier.startswith("@"):
                    target_user = await client.get_users(identifier)
            except Exception as e:
                logger.warning(f"Gagal mendapatkan target user dari argumen: {e}")

        if not target_user:
            await message.reply_text("Gunakan: `/unmute [reply ke user atau user_id/username]`")
            return

        try:
            permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            await client.restrict_chat_member(chat_id, target_user.id, permissions)

            app.database.remove_mute(target_user.id, chat_id)

            await message.reply_text(f"✅ {target_user.mention} telah di-unmute.")
            logger.info(f"User {target_user.id} di-unmute dari grup {chat_id} oleh {admin_id}.")
            await send_log(app, chat_id,
                f"**UNMUTE**\n"
                f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)")
        except Exception as e:
            await message.reply_text(f"❌ Gagal meng-unmute {target_user.mention}: {e}")
            logger.error(f"Gagal meng-unmute user {target_user.id} di grup {chat_id}: {e}")