from pyrogram import Client, filters
from plugins.ai_handler import generate_ai_reply, get_ai_local_response, summarize_text_ai # BARU: summarize_text_ai
import logging

logger = logging.getLogger(__name__)

def register_ai_commands(app: Client):

    @app.on_message(filters.command("ai", prefixes="/") & filters.group)
    async def intro_ai(client, message):
        await message.reply("🤖 ModCore AI siap membantu! Pakai perintah /ask [pertanyaan].")
        logger.info("Intro AI dikirim.")

    @app.on_message(filters.command("ask", prefixes="/") & filters.group)
    async def ask_handler(client, message):
        if not getattr(app, "use_ai", False):
            await message.reply("❌ Fitur AI tidak aktif.")
            return

        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Gunakan: /ask [pertanyaan kamu]")
            return

        await message.reply("⏳ Sedang memproses...")

        if getattr(app, "ai_provider", "") == "openrouter":
            reply = await generate_ai_reply(query)
        else:
            reply = get_ai_local_response(query, app.ollama_model)

        await message.reply(reply)

    @app.on_message(filters.command("summarize", prefixes="/") & filters.group) # BARU
    async def summarize_chat_command(client, message):
        if not getattr(app, "use_ai", False):
            await message.reply("❌ Fitur AI tidak aktif.")
            return

        if not message.reply_to_message:
            await message.reply("Gunakan perintah ini dengan me-reply pesan yang ingin diringkas.")
            return

        # Ambil teks dari pesan yang di-reply
        text_to_summarize = message.reply_to_message.text
        if not text_to_summarize:
            await message.reply("Pesan yang di-reply tidak mengandung teks.")
            return

        await message.reply("⏳ Sedang meringkas teks...")

        try:
            summary = await summarize_text_ai(text_to_summarize, app.ai_provider, app.ollama_model)
            await message.reply(f"📝 **Ringkasan:**\n\n{summary}")
            logger.info(f"Teks diringkas untuk {message.from_user.id}.")
        except Exception as e:
            await message.reply(f"❌ Gagal meringkas teks: {e}")
            logger.error(f"Gagal meringkas teks untuk {message.from_user.id}: {e}")
