import os
import logging
from pyrogram import filters
from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ydl_opts = {
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'format': 'best',
    'quiet': True,
    'noplaylist': True,
}

def register(app):
    @app.on_message(filters.command("download", prefixes="/")) # Ditambahkan prefixes="/"
    async def download_handler(client, message):
        logger.info(f"Download command received from {message.from_user.id}. Command: {message.text}")
        if len(message.command) < 2:
            await message.reply("Gunakan format:\n`/download [link video atau musik]`", quote=True)
            return
        
        url = message.command[1]
        await message.reply(f"⏳ Sedang memproses download:\n{url}", quote=True)

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            await message.reply_document(filename, caption=f"✅ Selesai!\nJudul: {info.get('title')}")
            logger.info(f"File {filename} berhasil dikirim.")

            os.remove(filename)

        except Exception as e:
            logger.error(f"Gagal download: {e}")
            await message.reply(f"❌ Gagal download:\n{e}", quote=True)

