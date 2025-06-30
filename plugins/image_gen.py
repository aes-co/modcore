from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from utils.hf_image_gen import generate_image_hf # Import fungsi dari utilitas baru
import io # Untuk menangani byte gambar

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("genimage", prefixes="/") & filters.group)
    async def generate_image_command(client: Client, message: Message):
        if not app.hf_api_token:
            await message.reply("❌ Fitur generasi gambar tidak aktif. HF_API_TOKEN belum diatur.")
            return

        prompt = " ".join(message.command[1:])
        if not prompt:
            await message.reply("Gunakan: `/genimage [deskripsi gambar yang diinginkan]`")
            return

        await message.reply("⏳ Sedang menghasilkan gambar... Ini mungkin memakan waktu beberapa detik.")
        logger.info(f"Permintaan genimage dari {message.from_user.id} dengan prompt: {prompt}")

        try:
            image_bytes = await generate_image_hf(prompt)
            if image_bytes:
                # Kirim gambar sebagai file in-memory
                await message.reply_photo(io.BytesIO(image_bytes), caption=f"✅ Gambar dihasilkan untuk: `{prompt}`")
                logger.info(f"Gambar berhasil dikirim untuk {message.from_user.id}.")
            else:
                await message.reply("❌ Gagal menghasilkan gambar. Pastikan deskripsi tidak terlalu kompleks atau coba lagi nanti.")
                logger.warning(f"Gagal menghasilkan gambar untuk {message.from_user.id} dengan prompt: {prompt}. Image bytes kosong.")
        except Exception as e:
            await message.reply(f"❌ Terjadi kesalahan saat menghasilkan gambar: {e}")
            logger.error(f"Error saat generasi gambar untuk {message.from_user.id}: {e}", exc_info=True)
