from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import logging
import asyncio

logger = logging.getLogger(__name__)

def register(app: Client):

    @app.on_message(filters.command("tagall", prefixes="/") & filters.group)
    async def tagall_handler(client: Client, message: Message):
        chat_id = message.chat.id
        sender = message.from_user

        # Cek apakah admin
        try:
            member = await client.get_chat_member(chat_id, sender.id)
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await message.reply_text("❌ Hanya admin yang dapat menggunakan perintah ini.")
                return
        except Exception as e:
            logger.error(f"Gagal memverifikasi admin: {e}")
            return

        # Ambil teks tambahan jika ada
        custom_text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""

        await message.reply_text("🔍 Mengumpulkan data anggota...")
        mentions = []
        count = 0
        batch = []

        async for user in client.get_chat_members(chat_id):
            if user.user.is_bot:
                continue

            name = user.user.first_name or "User"
            mention = user.user.mention(name=name)
            batch.append(mention)
            count += 1

            # Kirim setiap 5 mention
            if len(batch) == 5:
                tag_text = custom_text + "\n\n" + " ".join(batch) if custom_text else " ".join(batch)
                try:
                    await message.reply_text(tag_text)
                    await asyncio.sleep(1.5)
                except Exception as e:
                    logger.warning(f"Gagal kirim mention batch: {e}")
                batch = []

            if count >= 100:
                break  # Hindari terlalu banyak spam

        # Kirim sisa mention
        if batch:
            tag_text = custom_text + "\n\n" + " ".join(batch) if custom_text else " ".join(batch)
            try:
                await message.reply_text(tag_text)
            except Exception as e:
                logger.warning(f"Gagal kirim mention akhir: {e}")

        logger.info(f"{sender.id} menggunakan /tagall di grup {chat_id} untuk {count} member.")
