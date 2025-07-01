from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("report") & filters.group)
    async def report_user(client: Client, message: Message):
        chat_id = message.chat.id
        user = message.from_user

        if not message.reply_to_message:
            await message.reply_text("❗ Balas pesan pengguna yang ingin kamu laporkan.")
            return

        reported_user = message.reply_to_message.from_user
        mention = reported_user.mention if reported_user else "Pengguna tidak dikenal"

        try:
            admins = await client.get_chat_members(chat_id, filter="administrators")
            admin_mentions = [f"[{admin.user.first_name}](tg://user?id={admin.user.id})" for admin in admins if not admin.user.is_bot]

            admin_text = ", ".join(admin_mentions)
            await message.reply_text(
                f"🚨 {user.mention} telah melaporkan {mention} ke admin!\n"
                f"👮 Panggilan untuk admin: {admin_text}",
                disable_web_page_preview=True
            )

            logger.info(f"{user.id} melaporkan {reported_user.id if reported_user else 'UNKNOWN'} di grup {chat_id}")
        except Exception as e:
            logger.error(f"Error saat menjalankan /report: {e}")
            await message.reply_text("❌ Terjadi kesalahan saat memproses laporan.")
