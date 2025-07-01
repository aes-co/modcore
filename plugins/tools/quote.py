from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("quote"))
async def quote_handler(client: Client, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply_text("❌ Balas pesan teks yang ingin dijadikan quote.")

    text = reply.text
    user = reply.from_user.mention
    quote = f"❝ {text} ❞\n\n— {user}"

    await message.reply_text(quote)

    logger.info(f"{message.from_user.id} mengutip pesan dari {reply.from_user.id}")
    await send_log(client, message.chat.id,
        f"**QUOTE**\n"
        f"👤 Pengutip: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"📨 Dari: {user} (`{reply.from_user.id}`)\n"
        f"📝 Isi: `{text}`"
    )
