from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import ChatMemberUpdatedHandler
from pyrogram.enums import ChatMemberStatus
import logging
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

# Penyimpanan sementara pesan welcome
# Kalau mau permanen, sebaiknya pindah ke database
welcome_messages = {}

def register(app: Client):

    @app.on_message(filters.command("setwelcome") & filters.group)
    async def set_welcome(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Setwelcome command in {chat_id} by {admin_id}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang bisa mengatur pesan welcome.")
            return

        if len(message.command) < 2:
            await message.reply_text("Gunakan: `/setwelcome [pesan selamat datang]`")
            return

        welcome_text = " ".join(message.command[1:])
        welcome_messages[chat_id] = welcome_text

        await message.reply_text("✅ Pesan welcome berhasil disimpan.")
        logger.info(f"Welcome message set in group {chat_id} by {admin_id}")
        await send_log(app, chat_id,
            f"**SET WELCOME**\n"
            f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
            f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
            f"**Pesan Baru:** {welcome_text}"
        )

    @app.on_message(filters.command("welcome") & filters.group)
    async def show_welcome(client: Client, message: Message):
        chat_id = message.chat.id
        welcome_text = welcome_messages.get(chat_id)

        if not welcome_text:
            await message.reply_text("ℹ️ Pesan welcome belum diatur.")
        else:
            await message.reply_text(f"👋 **Pesan Welcome:**\n\n{welcome_text}")

    @app.on_chat_member_updated()
    async def greet_new_member(client: Client, chat_member):
        chat_id = chat_member.chat.id
        new_user = chat_member.new_chat_member.user

        if (
            chat_member.old_chat_member.status == ChatMemberStatus.LEFT
            and chat_member.new_chat_member.status == ChatMemberStatus.MEMBER
        ):
            welcome_text = welcome_messages.get(chat_id)
            if welcome_text:
                try:
                    await client.send_message(
                        chat_id,
                        welcome_text.replace("{name}", new_user.mention),
                        disable_web_page_preview=True
                    )
                    logger.info(f"Sent welcome message to {new_user.id} in {chat_id}")
                except Exception as e:
                    logger.error(f"Gagal mengirim welcome message: {e}")
