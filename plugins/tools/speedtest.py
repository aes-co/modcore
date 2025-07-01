import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import speedtest
from utils.telegram_helpers import is_admin_or_creator

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("speedtest") & (filters.private | filters.group))
    async def run_speedtest(client: Client, message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if message.chat.type in ["group", "supergroup"]:
            if not await is_admin_or_creator(client, chat_id, user_id):
                await message.reply_text("❌ Hanya admin yang bisa menjalankan perintah ini di grup.")
                return

        logger.info(f"Speedtest command by {user_id} in chat {chat_id}")

        sent = await message.reply_text("🔄 Sedang menjalankan speedtest, mohon tunggu...")

        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download()
            upload = st.upload()
            ping = st.results.ping

            result = (
                f"📊 **Hasil Speedtest**\n"
                f"🏓 **Ping:** `{ping:.2f} ms`\n"
                f"📥 **Download:** `{download / 1024 / 1024:.2f} Mbps`\n"
                f"📤 **Upload:** `{upload / 1024 / 1024:.2f} Mbps`\n"
            )
            await sent.edit_text(result)
            logger.info(f"Speedtest result for {user_id}:\nPing: {ping:.2f}ms, DL: {download:.2f}, UL: {upload:.2f}")
        except Exception as e:
            await sent.edit_text(f"❌ Gagal menjalankan speedtest: {e}")
            logger.error(f"Speedtest failed: {e}")
