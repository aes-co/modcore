from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("demote") & filters.group)
async def demote_handler(client: Client, message: Message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    admin = message.from_user

    if not reply:
        return await message.reply_text("❌ Balas pesan user yang ingin di-demote.")

    target = reply.from_user
    try:
        await client.promote_chat_member(
            chat_id,
            target.id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_video_chats=False,
            can_manage_chat=False
        )
        await message.reply_text(f"✅ {target.mention} telah di-demote.")
        logger.info(f"{admin.id} menurunkan admin {target.id} di grup {chat_id}")
        await send_log(client, chat_id,
            f"**DEMOTE**\n"
            f"👤 Admin: {admin.mention} (`{admin.id}`)\n"
            f"📤 Target: {target.mention} (`{target.id}`)\n"
            f"📍 Grup: {message.chat.title} (`{chat_id}`)"
        )
    except ChatAdminRequired:
        await message.reply_text("❌ Bot tidak memiliki izin yang cukup untuk demote.")
        logger.warning(f"Demote gagal: tidak cukup izin di {chat_id}")
