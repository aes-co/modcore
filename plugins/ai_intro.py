from pyrogram import Client, filters
import logging

logger = logging.getLogger(__name__)

def register_intro(app: Client):
    @app.on_message(filters.command("ai", prefixes="/") & filters.group) # Ditambahkan prefixes="/" dan filters.group
    async def ai_intro(client, message):
        logger.info(f"AI intro command received from {message.from_user.id}.")
        await message.reply(
            "**Hello, I am ModCore AI Bot.**\n"
            "Aku gabungan berbagai fitur dengan AI-powered simplicity. 🤖✨\n\n"
            "_Gunakan /ping untuk tes koneksi._"
        )

