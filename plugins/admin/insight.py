from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("insight") & filters.group)
async def insight_handler(client: Client, message: Message):
    chat = message.chat
    chat_id = chat.id

    try:
        members_count = await client.get_chat_members_count(chat_id)
        admins = await client.get_chat_members(chat_id, filter="administrators")
        bots = 0
        async for m in client.get_chat_members(chat_id):
            if m.user.is_bot:
                bots += 1

        text = (
            f"📊 **Insight Grup**\n"
            f"🏷️ Nama Grup: {chat.title}\n"
            f"🆔 ID Grup: `{chat.id}`\n"
            f"👥 Jumlah Anggota: `{members_count}`\n"
            f"🛡️ Jumlah Admin: `{len(list(admins))}`\n"
            f"🤖 Jumlah Bot: `{bots}`"
        )
        await message.reply_text(text)

        logger.info(f"{message.from_user.id} meminta insight grup {chat_id}")
        await send_log(client, chat_id,
            f"**GROUP INSIGHT**\n"
            f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"📍 Grup: {chat.title} (`{chat_id}`)\n"
            f"👥 Anggota: {members_count}, Admin: {len(list(admins))}, Bot: {bots}"
        )

    except Exception as e:
        await message.reply_text("❌ Gagal mengambil insight grup.")
        logger.error(f"Insight gagal di {chat_id}: {e}")
