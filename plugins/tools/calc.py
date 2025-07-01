from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.telegram_helpers import send_log

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("calc"))
async def calc_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Kirim seperti ini:\n`/calc 1+1*2`", quote=True)

    expression = message.text.split(None, 1)[1]

    try:
        if not all(c in "0123456789+-*/(). " for c in expression):
            return await message.reply_text("❌ Hanya karakter angka dan operator dasar yang diizinkan.", quote=True)

        result = eval(expression)
        await message.reply_text(f"🧮 Hasil:\n`{expression} = {result}`")

        logger.info(f"{message.from_user.id} melakukan kalkulasi: {expression} = {result}")
        await send_log(client, message.chat.id,
            f"**KALKULASI**\n"
            f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"🧮 Ekspresi: `{expression}`\n"
            f"✅ Hasil: `{result}`"
        )

    except Exception as e:
        await message.reply_text(f"⚠️ Error saat menghitung: `{e}`")
        logger.warning(f"Kalkulasi gagal oleh {message.from_user.id}: {expression} - {e}")
