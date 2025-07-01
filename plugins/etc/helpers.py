from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

async def get_target_user(message: Message):
    """Mendapatkan target user dari argumen perintah atau dari pesan yang dibalas."""
    target_user = None
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            target_id = message.command[1]
            if target_id.isdigit():
                target_user = await message._client.get_users(int(target_id))
            elif target_id.startswith('@'):
                target_user = await message._client.get_users(target_id)
        except Exception as e:
            logger.warning(f"Gagal mendapatkan target user dari argumen: {e}")
            pass
    return target_user
