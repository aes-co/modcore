from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("promote") & filters.group)
async def promote_handler(client: Client, message: Message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    admin = message.from_user

    if not reply:
        return await message.reply_text("❌ Balas pesan user yang ingin di-promote.")

    target = reply.from_user
    try:
        await client.promote_chat_member(
            chat_id,
            target.id,
            can_change_info=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False,
            can_manage_video_chats=True,
            can_manage_chat=True
        )
        await message.reply_text(f"✅ {target.mention} telah dipromosikan sebagai admin.")
        logger.info(f"{admin.id} promote {target.id} di grup {chat_id}")
        await send_log(client, chat_id,
            f"**PROMOTE**
"
            f"👤 Admin: {admin.mention} (`{admin.id}`)
"
            f"👥 Target: {target.mention} (`{target.id}`)
"
            f"📍 Grup: {message.chat.title} (`{chat_id}`)"
        )
    except ChatAdminRequired:
        await message.reply_text("❌ Bot tidak memiliki izin yang cukup untuk promote.")
        logger.warning(f"Promote gagal: tidak cukup izin di {chat_id}")