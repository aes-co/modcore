from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import is_admin_or_creator

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("log") & filters.group)
    async def log_info(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin grup yang bisa menggunakan perintah ini.")
            return

        group_settings = app.database.get_group_settings(chat_id)
        log_channel_id = group_settings.get("log_channel_id")

        if log_channel_id:
            try:
                channel_info = await client.get_chat(log_channel_id)
                await message.reply_text(
                    f"📦 **Channel Log Saat Ini:**\n"
                    f"- **Nama:** {channel_info.title}\n"
                    f"- **ID:** `{log_channel_id}`\n\n"
                    "Kirim pesan tes ke channel log? Gunakan: `/log test`"
                )
                logger.info(f"Log channel info ditampilkan oleh {admin_id} di grup {chat_id}")
            except Exception as e:
                await message.reply_text(f"❌ Gagal mengakses channel log: {e}")
                logger.error(f"Log channel tidak bisa diakses untuk grup {chat_id}: {e}")
        else:
            await message.reply_text("ℹ️ Channel log belum diatur di grup ini.\nGunakan `/setlogchannel` untuk mengaturnya.")

        if len(message.command) > 1 and message.command[1].lower() == "test":
            if log_channel_id:
                try:
                    await client.send_message(
                        log_channel_id,
                        f"✅ Pesan log uji berhasil dikirim dari grup **{message.chat.title}** (`{chat_id}`)"
                    )
                    await message.reply_text("✅ Pesan log uji berhasil dikirim ke channel log.")
                except Exception as e:
                    await message.reply_text(f"❌ Gagal mengirim pesan uji ke channel log: {e}")
                    logger.error(f"Gagal kirim log test dari grup {chat_id}: {e}")
