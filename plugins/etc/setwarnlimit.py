
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_setwarnlimit(app: Client):

    @app.on_message(filters.command("setwarnlimit", prefixes="/") & filters.group)
    async def set_warn_limit(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"SETWARNLIMIT command received in group {chat_id} by {admin_id}. Command: {message.text}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_limit = group_settings.get("warn_limit", 3)
            await message.reply_text(f"Batas peringatan saat ini adalah **{current_limit}**.\n"
                                     "Gunakan: `/setwarnlimit [angka]`")
            return

        try:
            new_limit = int(message.command[1])
            if new_limit < 1:
                await message.reply_text("❌ Batas peringatan harus angka positif (minimal 1).")
                return

            app.database.update_group_setting(chat_id, "warn_limit", new_limit)
            await message.reply_text(f"✅ Batas peringatan berhasil diatur menjadi **{new_limit}**.")
            logger.info(f"Batas peringatan di grup {chat_id} diatur menjadi {new_limit} oleh {admin_id}.")
            await send_log(app, chat_id,
                f"**SET WARN LIMIT**\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                f"**Batas Baru:** {new_limit}")
        except ValueError:
            await message.reply_text("❌ Batas peringatan harus berupa angka.")
