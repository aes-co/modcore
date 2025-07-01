from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import is_admin_or_creator, send_log

logger = logging.getLogger(__name__)

# Menyimpan sementara aturan di memori
# Jika ingin disimpan permanen, integrasikan ke database
group_rules = {}

def register(app: Client):

    @app.on_message(filters.command("setrules") & filters.group)
    async def set_rules(client: Client, message: Message):
        chat_id = message.chat.id
        admin_id = message.from_user.id

        logger.info(f"Setrules command in {chat_id} by {admin_id}")

        if not await is_admin_or_creator(client, chat_id, admin_id):
            await message.reply_text("❌ Hanya admin yang bisa mengatur aturan.")
            return

        if len(message.command) < 2:
            await message.reply_text("Gunakan: `/setrules [isi aturan grup]`")
            return

        rules_text = " ".join(message.command[1:])
        group_rules[chat_id] = rules_text

        await message.reply_text("✅ Aturan grup berhasil diperbarui.")
        logger.info(f"Rules for group {chat_id} set by {admin_id}")
        await send_log(app, chat_id,
            f"**SET RULES**\n"
            f"**Admin:** {message.from_user.mention} (`{admin_id}`)\n"
            f"**Grup:** {message.chat.title} (`{chat_id}`)\n"
            f"**Isi Aturan:**\n{rules_text}"
        )

    @app.on_message(filters.command("rules") & filters.group)
    async def show_rules(client: Client, message: Message):
        chat_id = message.chat.id
        logger.info(f"Rules requested in {chat_id} by {message.from_user.id}")

        rules_text = group_rules.get(chat_id)
        if not rules_text:
            await message.reply_text("ℹ️ Aturan belum diatur di grup ini.")
        else:
            await message.reply_text(f"📜 **Aturan Grup:**\n\n{rules_text}")
