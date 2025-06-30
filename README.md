
# 🤖 ModCore Bot - Telegram Multifungsi Modular

**ModCore Bot** adalah bot Telegram serbaguna dengan arsitektur modular yang dirancang untuk fleksibilitas dan kemudahan pengembangan.  
Bot ini dilengkapi dengan berbagai fitur canggih, mulai dari interaksi AI, pengunduh media, sistem moderasi grup yang komprehensif, hingga integrasi donasi.

**Owner:** [@aesneverhere](https://t.me/aesneverhere)  
**Support Donasi:** [Saweria](https://saweria.co/aesneverhere)

---

## ✨ Fitur Utama

- **Interaksi AI Cerdas**
- **Pengunduh Media Universal**
- **Sistem Donasi Terintegrasi**
- **Manajemen Grup Komprehensif (Moderasi)**
- **Pesan Selamat Datang & Selamat Tinggal Kustom**
- **Cek Status Bot**
- **Arsitektur Modular & Mudah Dikembangkan**
- **Auto Cookies Generator (Untuk Pengembangan Lanjutan)**

---

## 📥 Instalasi

### Persiapan
Pastikan Anda memiliki **Python 3.8+** dan `pip` terinstal di sistem Anda.

```bash
# Clone repositori
git clone https://github.com/aesneverhere/modcore.git

# Masuk ke direktori proyek
cd modcore

# Berikan izin eksekusi pada script setup
chmod +x setup.sh

# Jalankan setup interaktif
./setup.sh
```

Script `setup.sh` akan menginstal dependensi dan membantu Anda membuat file `.env` untuk konfigurasi bot.

---

## ⚙️ Konfigurasi .env

Setelah menjalankan `setup.sh`, isi file `.env` seperti berikut:

### Wajib
```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=1234567890:ABCDEF-1234567890abcdef-1234567890
USERNAME=MyAwesomeBot
```

- **API_ID & API_HASH:** Dapatkan dari [my.telegram.org](https://my.telegram.org).
- **BOT_TOKEN:** Dapatkan dari @BotFather.
- **USERNAME:** Username bot Anda (tanpa @).

### Opsional
```env
USE_AI=True
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-abcdef1234567890abcdef1234567890
LINK_DONASI_SAWERIA=https://saweria.co/aesneverhere
SHRINKME_API_TOKEN=your_shrinkme_api_token_here
```

- **USE_AI:** Aktifkan AI dengan `True`.
- **AI_PROVIDER:** Pilih `openrouter` atau `ollama`.
- **OPENROUTER_API_KEY:** Diperlukan jika AI_PROVIDER adalah `openrouter`.
- **LINK_DONASI_SAWERIA:** Link donasi Anda.
- **SHRINKME_API_TOKEN:** Token API ShrinkMe untuk shortlink.

---

## 🚀 Menjalankan Bot

```bash
python3 main.py
```

Bot Anda sekarang akan aktif dan siap digunakan!

---

## 🧪 Tes Fitur Singkat

| Perintah              | Deskripsi                                        |
|-----------------------|--------------------------------------------------|
| `/start`              | Pesan selamat datang & daftar fitur              |
| `/ping`               | Cek status bot                                   |
| `/ask [pertanyaan]`   | Tanya AI                                         |
| `/ai`                 | Info AI                                          |
| `/download [link]`    | Download & kirim media                           |
| `/donasi`             | Info donasi & shortlink                          |
| `/antilink on/off`    | Aktif/nonaktifkan fitur anti-link di grup        |
| `/ban`, `/kick`       | Ban atau keluarkan pengguna                      |
| `/mute`, `/unmute`    | Mute/unmute pengguna                             |
| `/warn`, `/unwarn`    | Berikan atau hapus peringatan pengguna           |
| `/setwarnlimit`       | Atur batas peringatan                            |
| `/setlogchannel`      | Atur channel log                                 |
| `/setwelcome`         | Atur pesan sambutan                              |
| `/setwelcomebutton`   | Tambah tombol di pesan sambutan                  |
| `/setgoodbye`         | Atur pesan perpisahan                            |

---

## 📂 Struktur Proyek

```bash
modcore/
├── main.py
├── setup.sh
├── .env
├── plugins/
│   ├── ai.py
│   ├── download.py
│   ├── moderation.py
│   └── ...
└── README.md
```

---

## 💡 Kontribusi

Kontribusi sangat terbuka!  
Silakan fork, buat pull request, atau buka issue untuk saran/bug/fitur baru.

Jika ingin berdiskusi atau tanya-tanya, mention saya di [@aesneverhere](https://t.me/aesneverhere).

---

## 📜 Lisensi

[MIT License](https://choosealicense.com/licenses/mit/)
