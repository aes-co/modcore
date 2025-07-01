
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_unwarn(app: Client):

    @app.on_message(filters.command("unwarn", prefixes="/") & filters.group)
    async def unwarn_user(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"UNWARN command received in group {chat_id} by {admin_id}. Command: {message.text}")

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
            await message.reply_text("Gunakan: `/unwarn [reply ke user atau user_id/username]`")
            return

        app.database.clear_warns(chat_id, target_user.id)

        await message.reply_text(f"✅ Semua peringatan untuk {target_user.mention} telah dihapus.")
        logger.info(f"Semua peringatan untuk user {target_user.id} di grup {chat_id} dihapus oleh {admin_id}.")
        await send_log(app, chat_id,
            f"**UNWARN**\n"
            f"**User:** {target_user.mention} (`{target_user.id}`)\n"
            f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
            f"**Grup:** {message.chat.title} (`{chat_id}`)")
