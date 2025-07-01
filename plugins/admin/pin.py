from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command(["pin", "pinsilent"]) & filters.group)
    async def pin_message(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id
        command = message.command[0].lower()

        logger.info(f"Pin command received in group {chat_id} by {admin_id}: {command}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang dapat mem-pin pesan.")
            return

        if not message.reply_to_message:
            await message.reply_text("❌ Balas pesan yang ingin di-pin.\n\nGunakan: `/pin` atau `/pinSilent`.")
            return

        try:
            await client.pin_chat_message(
                chat_id,
                message.reply_to_message.id,
                disable_notification=(command == "pin" and False) or True
            )

            await message.reply_text("📌 Pesan berhasil di-pin.")
            logger.info(f"Pesan di-pin di grup {chat_id} oleh {admin_id}")
            await send_log(app, chat_id,
                f"**PIN**\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                f"**Silent:** {'Ya' if command == 'pinsilent' else 'Tidak'}"
            )

        except Exception as e:
            await message.reply_text(f"❌ Gagal mem-pin pesan: {e}")
            logger.error(f"Gagal pin pesan di grup {chat_id} oleh {admin_id}: {e}")
