
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import is_admin_or_creator, send_log
import logging

logger = logging.getLogger(__name__)

def register_setlogchannel(app: Client):

    @app.on_message(filters.command("setlogchannel", prefixes="/") & filters.group)
    async def set_log_channel(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"SETLOGCHANNEL command received in group {chat_id} by {admin_id}. Command: {message.text}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            current_log_channel = group_settings.get("log_channel_id")
            if current_log_channel:
                try:
                    channel_info = await app.get_chat(current_log_channel)
                    await message.reply_text(f"Channel log saat ini adalah **{channel_info.title}** (`{current_log_channel}`).\n"
                                             "Gunakan: `/setlogchannel [channel_id]` atau `/setlogchannel off` untuk menonaktifkan.")
                except Exception:
                    await message.reply_text(f"Channel log saat ini adalah ID **{current_log_channel}** (tidak dapat diakses).\n"
                                             "Gunakan: `/setlogchannel [channel_id]` atau `/setlogchannel off`.")
            else:
                await message.reply_text("Channel log belum diatur.\n"
                                         "Gunakan: `/setlogchannel [channel_id]` (forward pesan dari channel ke sini untuk mendapatkan ID) atau `/setlogchannel off`.")
            return

        channel_arg = message.command[1]
        if channel_arg.lower() == "off":
            app.database.update_group_setting(chat_id, "log_channel_id", None)
            await message.reply_text("✅ Channel log berhasil dinonaktifkan.")
            logger.info(f"Channel log di grup {chat_id} dinonaktifkan oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**LOG CHANNEL DISABLED**\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)")
        else:
            try:
                channel_id = int(channel_arg)
                try:
                    channel_info = await app.get_chat(channel_id)
                    if channel_info.type not in ["channel", "supergroup"]:
                        await message.reply_text("❌ ID yang diberikan bukan channel atau supergroup yang valid.")
                        return
                    app.database.update_group_setting(chat_id, "log_channel_id", channel_id)
                    await message.reply_text(f"✅ Channel log berhasil diatur ke **{channel_info.title}** (`{channel_id}`).")
                    logger.info(f"Channel log di grup {chat_id} diatur ke {channel_id} oleh {admin_id}.")
                    await send_log(app, chat_id,
                                   f"**LOG CHANNEL SET**\n"
                                   f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                                   f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                                   f"**Channel Log Baru:** {channel_info.title} (`{channel_id}`)")
                except Exception as e:
                    await message.reply_text(f"❌ Gagal memverifikasi channel ID. Pastikan bot adalah admin di channel tersebut dan ID-nya benar. Error: {e}")
                    logger.error(f"Gagal memverifikasi channel ID {channel_id} untuk grup {chat_id}: {e}")
            except ValueError:
                await message.reply_text("❌ Channel ID harus berupa angka. Forward pesan dari channel ke sini untuk mendapatkan ID-nya.")
