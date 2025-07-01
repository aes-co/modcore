from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("id"))
async def id_handler(client: Client, message: Message):
    user = message.from_user
    reply = message.reply_to_message

    if reply:
        target = reply.from_user
        user_id = target.id
        mention = target.mention
    else:
        user_id = user.id
        mention = user.mention

    chat_id = message.chat.id
    text = (
        f"🆔 **ID Info**\n"
        f"👤 User: {mention}\n"
        f"🧾 User ID: `{user_id}`\n"
        f"💬 Chat ID: `{chat_id}`"
    )
    await message.reply_text(text)

    logger.info(f"{user.id} mengecek ID (target: {user_id})")
    await send_log(client, chat_id,
        f"**ID CHECK**\n"
        f"👤 User: {mention} (`{user_id}`)\n"
        f"📍 Chat ID: `{chat_id}`"
    )
