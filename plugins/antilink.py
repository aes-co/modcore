from pyrogram import Client, filters
from pyrogram.types import Message
# from pyrogram.enums import ChatMemberStatus # Tidak perlu lagi di sini
import logging
import re
from utils.telegram_helpers import is_admin_or_creator # UBAH

logger = logging.getLogger(__name__)

# Regex untuk mendeteksi URL
URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|\([^\s()<>]+\))*\))+(?:\(([^\s()<>]+|\([^\s()<>]+\))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def register(app: Client):

    # Helper function to check if user is admin (sekarang diimpor)
    # async def is_admin_or_creator(client: Client, chat_id: int, user_id: int) -> bool:
    #     """Mengecek apakah pengguna adalah admin atau creator di grup."""
    #     try:
    #         member = await client.get_chat_member(chat_id, user_id)
    #         return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    #     except Exception as e:
    #         logger.error(f"Gagal mendapatkan status admin untuk user {user_id} di chat {chat_id}: {e}")
    #         return False

    @app.on_message(filters.text & filters.group & ~filters.via_bot & ~filters.regex(r"^\/"))
    async def anti_link_handler(client: Client, message: Message):
        logger.info(f"Anti-link handler triggered in group {message.chat.id} by {message.from_user.id}. Text: {message.text[:50]}...")
        
        chat_id = message.chat.id
        user_id = message.from_user.id

        group_settings = app.database.get_group_settings(chat_id)
        if not group_settings["anti_link_enabled"]:
            return

        if await is_admin_or_creator(client, chat_id, user_id): # Gunakan yang diimpor
            return

        if re.search(URL_REGEX, message.text):
            try:
                await message.delete()
                logger.info(f"Link dihapus dari user {user_id} di grup {chat_id}: {message.text}")
            except Exception as e:
                logger.error(f"Gagal menghapus pesan link dari {user_id} di {chat_id}: {e}")

    @app.on_message(filters.command("antilink", prefixes="/") & filters.group)
    async def antilink_command_handler(client: Client, message: Message):
        logger.info(f"Antilink command received in group {message.chat.id} by {message.from_user.id}. Command: {message.text}")
        chat_id = message.chat.id
        user_id = message.from_user.id

        if not await is_admin_or_creator(client, chat_id, user_id): # Gunakan yang diimpor
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            group_settings = app.database.get_group_settings(chat_id)
            status = "aktif" if group_settings["anti_link_enabled"] else "tidak aktif"
            await message.reply_text(f"Fitur Anti-Link saat ini **{status}**.\n"
                                     "Gunakan `/antilink on` atau `/antilink off` untuk mengubah.")
            return

        action = message.command[1].lower()

        if action == "on":
            app.database.update_group_setting(chat_id, "anti_link_enabled", True)
            await message.reply_text("✅ Fitur Anti-Link berhasil diaktifkan.")
            logger.info(f"Anti-Link diaktifkan di grup {chat_id} oleh admin {user_id}.")
        elif action == "off":
            app.database.update_group_setting(chat_id, "anti_link_enabled", False)
            await message.reply_text("✅ Fitur Anti-Link berhasil dinonaktifkan.")
            logger.info(f"Anti-Link dinonaktifkan di grup {chat_id} oleh admin {user_id}.")
        else:
            await message.reply_text("❌ Perintah tidak valid. Gunakan `/antilink on` atau `/antilink off`.")
