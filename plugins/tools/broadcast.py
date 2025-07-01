from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import get_all_users  # fungsi ini ambil semua user_id
from utils.telegram_helpers import send_log
import logging
import asyncio

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))  # pastikan OWNER_ID sudah didefinisikan
async def broadcast_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Kirim seperti ini:\n`/broadcast isi pesannya`", quote=True)

    text = message.text.split(None, 1)[1]
    users = await get_all_users()
    success = failed = 0

    await message.reply_text(f"📢 Mengirim pesan ke {len(users)} pengguna...")

    for user_id in users:
        try:
            await client.send_message(user_id, text)
            success += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1

    await message.reply_text(f"✅ Selesai!\nBerhasil: {success}\nGagal: {failed}")

    logger.info(f"Broadcast oleh {message.from_user.id}. Sukses: {success}, Gagal: {failed}")
    await send_log(client, message.chat.id,
        f"**BROADCAST**\n"
        f"👮 Admin: {message.from_user.mention} (`{message.from_user.id}`)\n"
        f"📝 Isi: `{text}`\n"
        f"✅ Berhasil: {success}\n"
        f"❌ Gagal: {failed}"
    )
