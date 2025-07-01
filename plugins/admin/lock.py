from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import logging
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("lock") & filters.group)
    async def lock_group(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Lock command received in group {chat_id} by {admin_id}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang dapat mengunci grup.")
            return

        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions()
            )

            await message.reply_text("🔒 Grup telah dikunci. Hanya admin yang dapat mengirim pesan.")
            logger.info(f"Grup {chat_id} berhasil dikunci oleh {admin_id}")
            await send_log(app, chat_id,
                f"**LOCKED**\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                f"**Status:** 🔒 Dikunci (tidak ada izin kirim pesan untuk member)"
            )

        except Exception as e:
            await message.reply_text(f"❌ Gagal mengunci grup: {e}")
            logger.error(f"Gagal mengunci grup {chat_id} oleh {admin_id}: {e}")

    @app.on_message(filters.command("unlock") & filters.group)
    async def unlock_group(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Unlock command received in group {chat_id} by {admin_id}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang dapat membuka kunci grup.")
            return

        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )

            await message.reply_text("🔓 Grup telah dibuka kembali.")
            logger.info(f"Grup {chat_id} berhasil dibuka oleh {admin_id}")
            await send_log(app, chat_id,
                f"**UNLOCKED**\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                f"**Status:** 🔓 Dibuka kembali"
            )

        except Exception as e:
            await message.reply_text(f"❌ Gagal membuka kunci grup: {e}")
            logger.error(f"Gagal membuka kunci grup {chat_id} oleh {admin_id}: {e}")
