from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("demote") & filters.group)
    async def demote_user(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Demote command received in {chat_id} by {admin_id}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang dapat mencabut status admin.")
            return

        if not message.reply_to_message:
            await message.reply_text("⚠️ Balas pesan pengguna yang ingin dicabut status admin-nya.")
            return

        target_user = message.reply_to_message.from_user

        try:
            await client.promote_chat_member(
                chat_id,
                target_user.id,
                can_change_info=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False
            )

            await message.reply_text(f"✅ {target_user.mention} telah dicabut status admin-nya.")
            logger.info(f"User {target_user.id} dicabut status admin oleh {admin_id} di {chat_id}")

            await send_log(app, chat_id,
                f"**DEMOTE**\n"
                f"**User:** {target_user.mention} (`{target_user.id}`)\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)")
        except Exception as e:
            await message.reply_text(f"❌ Gagal mencabut status admin {target_user.mention}: {e}")
            logger.error(f"Gagal demote {target_user.id} di {chat_id}: {e}")
