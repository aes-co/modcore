from pyrogram import Client, filters
from utils.shortlink import generate_shrinkme_link
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

LINK_DONASI = os.getenv("LINK_DONASI_SAWERIA")  # Isi di .env: https://saweria.co/aesneverhere

def register(app: Client):

    @app.on_message(filters.command("donasi", prefixes="/") & filters.group) # Ditambahkan prefixes="/" dan filters.group
    async def donasi_handler(client, message):
        logger.info(f"Donasi command received from {message.from_user.id}.")
        if not LINK_DONASI:
            await message.reply("⚠️ Link donasi belum diatur, hubungi admin.")
            return
        
        shortlink = generate_shrinkme_link(LINK_DONASI)
        
        if shortlink:
            teks = (
                "🙏 **Dukung pengembangan ModCore Bot!**\n\n"
                "Setiap donasi kamu sangat berarti untuk kelangsungan project ini.\n"
                f"🔗 Link donasi cepat: {shortlink}\n\n"
                "💡 Alternatif lain:\n"
                f"• Saweria langsung: [Klik di sini]({LINK_DONASI})\n"
                "• Kontak owner: @aesneverhere untuk metode lain\n\n"
                "Terima kasih banyak atas support kamu! 💜✨"
            )
        else:
            teks = (
                "⚠️ Gagal generate shortlink donasi.\n"
                f"Kamu bisa tetap donasi via Saweria:\n{LINK_DONASI}\n"
                "Atau kontak @aesneverhere untuk info lebih lanjut."
            )
        
        await message.reply(teks, disable_web_page_preview=True)
        logger.info("Pesan donasi dikirim.")

