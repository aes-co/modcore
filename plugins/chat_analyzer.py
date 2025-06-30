# FileName: /plugins/chat_analyzer.py
from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from collections import Counter
import re
import time

logger = logging.getLogger(__name__)

def register(app: Client):

    # PERBAIKAN DI SINI: Tambahkan daftar command yang ingin di-exclude
    excluded_commands = ["start", "help", "learn"]  # Sesuaikan dengan commands yang ada di bot
    
    # Handler untuk mengumpulkan data chat (FIXED)
    @app.on_message(
        filters.group & 
        ~filters.via_bot & 
        ~filters.command(excluded_commands)  # Sekarang sudah memiliki argumen
    )
    async def collect_chat_data(client: Client, message: Message):
        try:
            chat_id = message.chat.id
            user_id = message.from_user.id
            username = message.from_user.username if message.from_user.username else message.from_user.first_name
            
            message_type = "text"
            content = ""

            if message.text:
                content = message.text
            elif message.sticker:
                message_type = "sticker"
                content = message.sticker.emoji if message.sticker.emoji else "random_sticker"
            elif message.photo:
                message_type = "photo"
                content = message.caption if message.caption else "photo"
            elif message.animation:
                message_type = "gif"
                content = message.caption if message.caption else "gif"
            elif message.video:
                message_type = "video"
                content = message.caption if message.caption else "video"
            elif message.audio:
                message_type = "audio"
                content = message.audio.title if message.audio.title else "audio"
            elif message.voice:
                message_type = "voice"
                content = "voice_message"
            elif message.document:
                message_type = "document"
                content = message.document.file_name if message.document.file_name else "document"
            
            if content:
                app.database.add_chat_data(chat_id, user_id, username, message_type, content.lower())
                logger.debug(f"Chat data collected: {username}, {message_type}, '{content[:20]}...'")
                
        except Exception as e:
            logger.error(f"Error collecting chat data: {e}", exc_info=True)

    @app.on_message(filters.command("learn") & filters.group)
    async def learn_command(client: Client, message: Message):
        try:
            chat_id = message.chat.id
            logger.info(f"Learn command from {message.from_user.id} in {chat_id}")
            
            msg = await message.reply("🔄 Menganalisis data chat...")
            
            chat_data = app.database.get_chat_data(chat_id)
            
            if not chat_data:
                await msg.edit_text("❌ Belum ada data chat yang cukup.")
                return

            # [Analisis data tetap sama seperti sebelumnya]
            response = "📊 Hasil Analisis:\n"
            
            # Hitung pengguna aktif
            user_counts = Counter([d['username'] for d in chat_data])
            if user_counts:
                top_user = user_counts.most_common(1)[0]
                response += f"👤 Top user: {top_user[0]} ({top_user[1]} pesan)\n"
            
            # Kirim hasil
            await msg.edit_text(response)
            
        except Exception as e:
            logger.error(f"Learn error: {e}", exc_info=True)
            await message.reply("❌ Gagal menganalisis. Coba lagi nanti.")
