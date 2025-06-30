from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

def register(app: Client):
    @app.on_message(filters.command("help", prefixes="/") & filters.group)
    async def help_command_group(client: Client, message: Message):
        logger.info(f"Help command received from {message.from_user.id} in group {message.chat.id}.")
        help_text = (
            "📚 **Daftar Perintah ModCore Bot:**\n\n"
            "**🤖 Fitur AI:**\n"
            "• `/ask [pertanyaan]` - Tanya AI.\n"
            "• `/ai` - Info tentang AI bot.\n"
            "• `/summarize` (balas pesan) - Meringkas pesan dengan AI.\n"
            "• `/generatewelcome [tema]` - Buat pesan selamat datang dengan AI.\n"
            "• `/generategoodbye [tema]` - Buat pesan selamat tinggal dengan AI.\n"
            "• `/deepsearch [pertanyaan/URL]` - Cari informasi mendalam dengan AI.\n"
            "• `/genimage [deskripsi]` - Buat gambar dari teks dengan AI.\n\n"
            "**⬇️ Media & Donasi:**\n"
            "• `/download [link]` - Unduh video/musik dari link.\n"
            "• `/donasi` - Info donasi untuk mendukung bot.\n\n"
            "**🛡️ Moderasi Grup:**\n"
            "• `/antilink on/off` - Aktifkan/nonaktifkan anti-link.\n"
            "• `/ban` (balas/ID/username) - Blokir pengguna.\n"
            "• `/kick` (balas/ID/username) - Keluarkan pengguna.\n"
            "• `/mute` (balas/ID/username) - Bisukan pengguna.\n"
            "• `/unmute` (balas/ID/username) - Batalkan bisu pengguna.\n"
            "• `/warn` (balas/ID/username) - Beri peringatan.\n"
            "• `/unwarn` (balas/ID/username) - Hapus peringatan.\n"
            "• `/setwarnlimit [angka]` - Atur batas peringatan.\n"
            "• `/setwarnaction [ban/mute/kick]` - Atur tindakan otomatis setelah batas peringatan.\n"
            "• `/setfloodlimit [pesan] [detik]` - Atur batas flood.\n"
            "• `/setspamdetection on/off` - Aktifkan/nonaktifkan deteksi spam.\n"
            "• `/addblacklistword [kata]` - Tambah kata terlarang.\n"
            "• `/removeblacklistword [kata]` - Hapus kata terlarang.\n"
            "• `/listblacklistwords` - Daftar kata terlarang.\n"
            "• `/setlogchannel [ID channel]` - Atur channel log moderasi.\n\n"
            "**👋 Pesan Otomatis:**\n"
            "• `/setwelcome [pesan]` - Atur pesan selamat datang.\n"
            "• `/setwelcomebutton [Teks] | [URL]` - Tambah tombol di pesan selamat datang.\n"
            "• `/setgoodbye [pesan]` - Atur pesan selamat tinggal.\n\n"
            "**🎲 Fitur Fun:**\n"
            "• `/learn` - Analisis kebiasaan chat anggota (fun).\n\n"
            "**⚙️ Lain-lain:**\n"
            "• `/ping` - Cek status bot.\n"
            "• `/start` - Pesan selamat datang awal.\n"
            "• `/help` - Menampilkan daftar perintah ini.\n\n"
            "Untuk detail lebih lanjut tentang penggunaan perintah, silakan kunjungi GitHub bot: [https://github.com/aesneverhere](https://github.com/aesneverhere)"
        )
        await message.reply_text(help_text, disable_web_page_preview=True)

    @app.on_message(filters.command("help", prefixes="/") & filters.private)
    async def help_command_private(client: Client, message: Message):
        logger.info(f"Help command received from {message.from_user.id} in private chat.")
        help_text = (
            "📚 **Daftar Perintah ModCore Bot:**\n\n"
            "**🤖 Fitur AI:**\n"
            "• `/ask [pertanyaan]` - Tanya AI.\n"
            "• `/ai` - Info tentang AI bot.\n"
            "• `/summarize` (balas pesan) - Meringkas pesan dengan AI.\n"
            "• `/generatewelcome [tema]` - Buat pesan selamat datang dengan AI.\n"
            "• `/generategoodbye [tema]` - Buat pesan selamat tinggal dengan AI.\n"
            "• `/deepsearch [pertanyaan/URL]` - Cari informasi mendalam dengan AI.\n"
            "• `/genimage [deskripsi]` - Buat gambar dari teks dengan AI.\n\n"
            "**⬇️ Media & Donasi:**\n"
            "• `/download [link]` - Unduh video/musik dari link.\n"
            "• `/donasi` - Info donasi untuk mendukung bot.\n\n"
            "**⚙️ Lain-lain:**\n"
            "• `/ping` - Cek status bot.\n"
            "• `/start` - Pesan selamat datang awal.\n"
            "• `/help` - Menampilkan daftar perintah ini.\n\n"
            "Untuk fitur moderasi grup, bot harus ditambahkan ke grup dan diberikan izin admin. "
            "Silakan kunjungi GitHub bot untuk detail lebih lanjut: [https://github.com/aesneverhere](https://github.com/aesneverhere)"
        )
        await message.reply_text(help_text, disable_web_page_preview=True)
