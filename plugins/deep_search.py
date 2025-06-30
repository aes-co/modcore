from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from plugins.ai_handler import generate_ai_reply, get_ai_local_response # Menggunakan fungsi AI yang sudah ada
from utils.web_scraper import scrape_text_from_url # BARU: Untuk Opsi 2

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("deepsearch", prefixes="/") & filters.group)
    async def deep_search_command(client: Client, message: Message):
        if not getattr(app, "use_ai", False):
            await message.reply("❌ Fitur Deep Search AI tidak aktif.")
            return

        query_parts = message.command[1:]
        if not query_parts:
            await message.reply("Gunakan: `/deepsearch [pertanyaan]` atau `/deepsearch [URL] [pertanyaan]`")
            return

        # Cek apakah argumen pertama adalah URL
        is_url_search = False
        url = None
        question = " ".join(query_parts)

        if len(query_parts) > 1 and (query_parts[0].startswith("http://") or query_parts[0].startswith("https://")):
            url = query_parts[0]
            question = " ".join(query_parts[1:])
            is_url_search = True
            if not question:
                await message.reply("Jika Anda memberikan URL, Anda juga harus memberikan pertanyaan.")
                return

        await message.reply("⏳ Sedang melakukan pencarian mendalam dengan AI...")
        logger.info(f"Deep Search dari {message.from_user.id}. Query: {question}, URL: {url}")

        try:
            if is_url_search:
                scraped_text = await scrape_text_from_url(url)
                if not scraped_text:
                    await message.reply(f"❌ Gagal mengambil konten dari URL: {url}. Pastikan URL valid dan dapat diakses.")
                    return
                
                # Batasi teks yang dikirim ke AI agar tidak terlalu panjang
                max_text_length = 4000 # Sesuaikan dengan batasan token model AI
                if len(scraped_text) > max_text_length:
                    scraped_text = scraped_text[:max_text_length] + "..."

                full_prompt = (
                    f"Berdasarkan teks berikut dari {url}, jawab pertanyaan: '{question}'. "
                    f"Jika informasi tidak ada dalam teks, nyatakan demikian. Gunakan bahasa Indonesia.\n\n"
                    f"Teks:\n{scraped_text}"
                )
            else:
                # Opsi 1: Menggunakan LLM untuk menjawab pertanyaan umum
                full_prompt = f"Jawab pertanyaan berikut secara mendalam dan informatif dalam bahasa Indonesia: '{question}'"

            if app.ai_provider == "openrouter":
                response = await generate_ai_reply(full_prompt)
            elif app.ai_provider == "ollama":
                response = get_ai_local_response(full_prompt, app.ollama_model)
            else:
                response = "[Fitur Deep Search AI tidak aktif atau provider tidak didukung.]"
            
            await message.reply(f"🔍 **Hasil Deep Search:**\n\n{response}", disable_web_page_preview=True)
            logger.info(f"Deep Search berhasil untuk {message.from_user.id}.")

        except Exception as e:
            await message.reply(f"❌ Terjadi kesalahan saat melakukan Deep Search: {e}")
            logger.error(f"Error saat Deep Search untuk {message.from_user.id}: {e}", exc_info=True)
