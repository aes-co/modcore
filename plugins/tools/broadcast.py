from pyrogram import Client, filters
from pyrogram.types import Message
import logging
import asyncio

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_command(client: Client, message: Message):
        sender_username = message.from_user.username
        bot_owner_username = app.config.get("username")

        if not sender_username or sender_username.lower() != bot_owner_username.lower():
            await message.reply_text("❌ Hanya owner bot yang dapat menggunakan perintah ini.")
            return

        if len(message.command) < 2:
            await message.reply_text("Gunakan: `/broadcast [pesan]`")
            return

        text_to_broadcast = message.text.split(None, 1)[1]
        sent_count = 0
        failed_count = 0

        await message.reply_text("🔄 Menyiarkan pesan...")

        async for dialog in client.get_dialogs():
            chat = dialog.chat
            if chat.type in ("group", "supergroup"):
                try:
                    await client.send_message(chat.id, text_to_broadcast)
                    sent_count += 1
                    await asyncio.sleep(0.3)  # Hindari limit
                except Exception as e:
                    logger.warning(f"Gagal broadcast ke {chat.title} ({chat.id}): {e}")
                    failed_count += 1

        logger.info(f"Broadcast selesai: Berhasil {sent_count}, Gagal {failed_count}")
        await message.reply_text(f"✅ Broadcast selesai.\n\n🟢 Berhasil: {sent_count}\n🔴 Gagal: {failed_count}")
