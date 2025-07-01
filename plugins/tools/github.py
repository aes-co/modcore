import httpx
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/users/"

@Client.on_message(filters.command("github"))
async def github_lookup(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Kirim seperti ini:\n`/github username`", quote=True)

    username = message.text.split(None, 1)[1]
    url = GITHUB_API_URL + username

    try:
        async with httpx.AsyncClient() as http:
            resp = await http.get(url)
            if resp.status_code != 200:
                return await message.reply_text("⚠️ Username tidak ditemukan.")

            data = resp.json()
            text = (
                f"👤 **{data.get('name', username)}** (`@{username}`)\n"
                f"📍 Lokasi: `{data.get('location', 'Tidak tersedia')}`\n"
                f"📦 Repositori Publik: `{data.get('public_repos', 0)}`\n"
                f"👥 Pengikut: `{data.get('followers', 0)}` | Mengikuti: `{data.get('following', 0)}`\n"
                f"🔗 [Profil GitHub]({data.get('html_url')})"
            )
            await message.reply_text(text)

            logger.info(f"User {message.from_user.id} cari GitHub: {username}")
            await send_log(client, message.chat.id,
                f"**GITHUB LOOKUP**\n"
                f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
                f"🔍 Username: `{username}`"
            )

    except Exception as e:
        logger.error(f"Error GitHub lookup oleh {message.from_user.id}: {e}")
        await message.reply_text("❌ Terjadi kesalahan saat mengambil data GitHub.")
