from pyrogram import Client, filters
from pyrogram.types import Message
import logging
import re
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.text & filters.group & ~filters.via_bot & ~filters.regex(r"^\/"))
    async def blacklist_word_filter(client: Client, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        text = message.text.lower()

        if await is_admin_or_creator(client, chat_id, user_id):
            return

        blacklist_words = app.database.get_blacklist_words(chat_id)
        if not blacklist_words:
            return

        for word in blacklist_words:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                try:
                    await message.delete()
                    await message.reply_text(
                        f"🚫 {message.from_user.mention}, pesan Anda mengandung kata terlarang dan telah dihapus."
                    )
                    logger.info(f"Pesan dari user {user_id} di grup {chat_id} dihapus karena mengandung kata terlarang: '{word}'.")
                    await send_log(app, chat_id,
                                   f"**PESAN DIHAPUS (BLACKLIST)**\n"
                                   f"**User:** {message.from_user.mention} (`{user_id}`)\n"
                                   f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                                   f"**Kata Terlarang:** `{word}`\n"
                                   f"**Pesan Asli:** `{message.text}`")
                    return
                except Exception as e:
                    logger.error(f"Gagal menghapus pesan blacklist dari {user_id} di {chat_id}: {e}")

    @app.on_message(filters.command("addblacklistword", prefixes="/") & filters.group)
    async def add_blacklist_word_command(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        # --- DEBUG START ---
        is_user_admin = await is_admin_or_creator(client, chat_id, admin_id)
        logger.info(f"DEBUG: User {admin_id} (sender) is_admin_or_creator: {is_user_admin} in chat {chat_id} for addblacklistword.")
        # --- DEBUG END ---

        if not is_user_admin:
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            await message.reply_text("Gunakan: `/addblacklistword [kata_terlarang]`")
            return

        word = " ".join(message.command[1:]).lower()
        if app.database.add_blacklist_word(chat_id, word):
            await message.reply_text(f"✅ Kata `{word}` berhasil ditambahkan ke daftar kata terlarang.")
            logger.info(f"Kata '{word}' ditambahkan ke blacklist grup {chat_id} oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**BLACKLIST WORD ADDED**\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Kata:** `{word}`")
        else:
            await message.reply_text(f"⚠️ Kata `{word}` sudah ada di daftar kata terlarang.")

    @app.on_message(filters.command("removeblacklistword", prefixes="/") & filters.group)
    async def remove_blacklist_word_command(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        # --- DEBUG START ---
        is_user_admin = await is_admin_or_creator(client, chat_id, admin_id)
        logger.info(f"DEBUG: User {admin_id} (sender) is_admin_or_creator: {is_user_admin} in chat {chat_id} for removeblacklistword.")
        # --- DEBUG END ---

        if not is_user_admin:
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            await message.reply_text("Gunakan: `/removeblacklistword [kata_terlarang]`")
            return

        word = " ".join(message.command[1:]).lower()
        if app.database.remove_blacklist_word(chat_id, word):
            await message.reply_text(f"✅ Kata `{word}` berhasil dihapus dari daftar kata terlarang.")
            logger.info(f"Kata '{word}' dihapus dari blacklist grup {chat_id} oleh {admin_id}.")
            await send_log(app, chat_id,
                           f"**BLACKLIST WORD REMOVED**\n"
                           f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
                           f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
                           f"**Kata:** `{word}`")
        else:
            await message.reply_text(f"⚠️ Kata `{word}` tidak ditemukan di daftar kata terlarang.")

    @app.on_message(filters.command("listblacklistwords", prefixes="/") & filters.group)
    async def list_blacklist_words_command(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        # --- DEBUG START ---
        is_user_admin = await is_admin_or_creator(client, chat_id, admin_id)
        logger.info(f"DEBUG: User {admin_id} (sender) is_admin_or_creator: {is_user_admin} in chat {chat_id} for listblacklistwords.")
        # --- DEBUG END ---

        if not is_user_admin:
            await message.reply_text("❌ Maaf, hanya admin grup yang bisa menggunakan perintah ini.")
            return

        words = app.database.get_blacklist_words(chat_id)
        if words:
            word_list = "\n".join([f"- `{w}`" for w in words])
            await message.reply_text(f"🚫 **Daftar Kata Terlarang di Grup Ini:**\n{word_list}")
        else:
            await message.reply_text("✅ Tidak ada kata terlarang yang diatur di grup ini.")
