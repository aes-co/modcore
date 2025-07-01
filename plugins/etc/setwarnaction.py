
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_setwarnaction(app: Client):

    @app.on_message(filters.command("setwarnaction", prefixes="/") & filters.group)
    async def set_warn_action(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"SETWARNACTION command received in group {chat_id} by {admin_id}. Command: {message.text}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_action = group_settings.get("warn_action", "ban")
            await message.reply_text(f"Tindakan otomatis setelah batas peringatan saat ini adalah **{current_action.upper()}**.\n"
                                     "Gunakan: `/setwarnaction [ban/mute/kick]`")
            return

        new_action = message.command[1].lower()
        if new_action not in ["ban", "mute", "kick"]:
            await message.reply_text("❌ Tindakan tidak valid. Pilihan: `ban`, `mute`, `kick`.")
            return

        app.database.update_group_setting(chat_id, "warn_action", new_action)
        await message.reply_text(f"✅ Tindakan otomatis setelah batas peringatan berhasil diatur menjadi **{new_action.upper()}**.")
        logger.info(f"Tindakan peringatan di grup {chat_id} diatur menjadi {new_action} oleh {admin_id}.")
        await send_log(app, chat_id,
            f"**SET WARN ACTION**\n"
            f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
            f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
            f"**Tindakan Baru:** {new_action.upper()}")
