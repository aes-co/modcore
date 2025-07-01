from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("purge") & filters.group)
    async def purge_messages(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Purge command received in group {chat_id} by {admin_id}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang dapat menggunakan perintah ini.")
            return

        if not message.reply_to_message:
            await message.reply_text("❌ Balas pesan pertama yang ingin kamu hapus massal.\n\nGunakan: `/purge` sebagai balasan.")
            return

        try:
            deleted = 0
            start_id = message.reply_to_message.id
            end_id = message.id

            for msg_id in range(start_id, end_id):
                try:
                    await client.delete_messages(chat_id, msg_id)
                    deleted += 1
                except Exception:
                    pass  # continue even if some messages can't be deleted

            await message.reply_text(f"🧹 Berhasil menghapus `{deleted}` pesan.")
            logger.info(f"{deleted} messages purged in group {chat_id} by {admin_id}")

            await send_log(app, chat_id,
                f"**PURGE**\n"
                f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                f"**Jumlah Pesan Dihapus:** {deleted}"
            )

        except Exception as e:
            await message.reply_text(f"❌ Gagal menghapus pesan: {e}")
            logger.error(f"Gagal melakukan purge di grup {chat_id} oleh {admin_id}: {e}")
