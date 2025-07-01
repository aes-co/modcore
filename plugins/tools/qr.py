import io
import qrcode
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("qr") & filters.private)
async def generate_qr(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Kirim seperti ini: `/qr teks atau link`", quote=True)

    text = message.text.split(None, 1)[1]
    img = qrcode.make(text)
    
    bio = io.BytesIO()
    bio.name = "qr.png"
    img.save(bio, "PNG")
    bio.seek(0)

    await message.reply_photo(bio, caption="✅ QR Code berhasil dibuat!")

    logger.info(f"{message.from_user.id} membuat QR dari: {text}")
    await send_log(client, message.chat.id,
        f"**QR Code Dibuat**\n"
        f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"📄 Teks: `{text}`"
    )
