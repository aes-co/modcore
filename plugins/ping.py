from pyrogram import Client, filters
import logging
import time # Import modul time

logger = logging.getLogger(__name__)

def register_ping_commands(app: Client):
    @app.on_message(filters.command("ping", prefixes="/"))
    async def ping_handler(client, message):
        start_time = time.time() # Catat waktu mulai
        
        # Kirim pesan awal untuk mendapatkan ID pesan
        initial_message = await message.reply("🔧 Pong!")
        
        end_time = time.time() # Catat waktu selesai
        response_time_ms = round((end_time - start_time) * 1000) # Hitung dalam milidetik
        
        await initial_message.edit_text(f"🔧 Pong! Bot aktif. (Respon dalam **{response_time_ms}ms**)")
        logger.info(f"Ping command dijawab untuk {message.from_user.id}. Respon dalam {response_time_ms}ms.")
