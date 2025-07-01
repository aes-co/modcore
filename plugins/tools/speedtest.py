import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.telegram_helpers import send_log
import logging
import time

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("speedtest"))
async def speedtest_handler(client: Client, message: Message):
    start = time.time()
    await message.reply_text("🔄 Sedang melakukan speedtest...")

    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download()
        upload_speed = st.upload()
        end = time.time()

        result = (
            f"📡 **Hasil Speedtest**\n"
            f"⬇️ Download: `{download_speed / 1024 / 1024:.2f} Mbps`\n"
            f"⬆️ Upload: `{upload_speed / 1024 / 1024:.2f} Mbps`\n"
            f"⏱️ Ping: `{st.results.ping} ms`\n"
            f"🕒 Waktu: `{end - start:.2f} detik`"
        )
        await message.reply_text(result)

        logger.info(f"{message.from_user.id} menjalankan speedtest")
        await send_log(client, message.chat.id,
            f"**SPEEDTEST**\n"
            f"👤 User: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"📡 Download: `{download_speed / 1024 / 1024:.2f} Mbps`\n"
            f"📤 Upload: `{upload_speed / 1024 / 1024:.2f} Mbps`\n"
            f"🏓 Ping: `{st.results.ping} ms`"
        )

    except Exception as e:
        await message.reply_text(f"❌ Speedtest gagal: {e}")
        logger.error(f"Speedtest error oleh {message.from_user.id}: {e}")
