from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
import logging

logger = logging.getLogger(__name__)

async def is_admin_or_creator(client: Client, chat_id: int, user_id: int) -> bool:
    """Mengecek apakah pengguna adalah admin atau creator di grup."""
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        logger.error(f"Gagal mendapatkan status admin untuk user {user_id} di chat {chat_id}: {e}")
        return False

async def send_log(app: Client, group_id: int, log_message: str):
    """Mengirim pesan log ke channel log grup jika diatur."""
    # Pastikan app.database sudah terpasang di main.py
    group_settings = app.database.get_group_settings(group_id)
    log_channel_id = group_settings.get("log_channel_id")
    if log_channel_id:
        try:
            await app.send_message(log_channel_id, log_message)
        except Exception as e:
            logger.error(f"Gagal mengirim log ke channel {log_channel_id} untuk grup {group_id}: {e}")
