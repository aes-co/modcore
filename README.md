<p align="center">
  <img src="https://github.com/images/mona-whisper.gif" alt="ModCore Cat Logo" width="150"/>
</p>

<h1 align="center">
  <b>ModCore — Powerful Modular Telegram Bot</b>
</h1>

<p align="center">
  <i>A blazing-fast, feature-rich, and highly modular Telegram bot framework for community management, automation, and AI interaction.</i>
</p>

<p align="center">
  <a href="https://github.com/aeswnh/modcore"><img src="https://img.shields.io/github/stars/aeswnh/modcore?style=flat-square&color=yellow" alt="Stars"/></a>
  <a href="https://github.com/aeswnh/modcore/fork"><img src="https://img.shields.io/github/forks/aeswnh/modcore?style=flat-square&color=orange" alt="Forks"/></a>
  <a href="https://github.com/aeswnh/modcore"><img src="https://img.shields.io/github/repo-size/aeswnh/modcore?style=flat-square&color=green" alt="Repo Size"/></a>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square" alt="Maintained"/>
</p>

---

## 🧠 Overview

**ModCore** adalah kerangka kerja bot Telegram modular berbasis Pyrogram. Dirancang untuk kemudahan ekspansi, kestabilan dalam grup besar, dan integrasi AI yang fleksibel.

---

## 🚀 Fitur Unggulan

* 🔹 **Plugin Modular** — Tambah, hapus, atau modifikasi fitur dengan mudah.
* 🤖 **AI Support** — Terhubung dengan OpenRouter, Ollama, HuggingFace.
* ⚡️ **Command Utility Lengkap** — Tools harian, moderasi, analitik.
* 📅 **Auto-setup .env** — Tidak perlu repot setup manual.
* 🎓 **Struktur bersih** — Terorganisir dan mudah dikembangkan.

---

## 🔧 Instalasi Cepat

```bash
git clone https://github.com/aeswnh/modcore && cd modcore
bash setup.sh
```

Masukkan konfigurasi `.env` saat diminta oleh terminal.

---

## 🧨 Register Bot via BotFather

1. Buka [@BotFather](https://t.me/BotFather)
2. Jalankan `/newbot`, masukkan nama dan username bot.
3. Salin token yang diberikan dan isi ke dalam `.env` saat setup.

---

## 📂 Struktur Proyek

```
modcore/
├── main.py            # Entry point bot
├── plugins/           # Modular commands (admin, tools, etc)
│   ├── admin/         # Fitur admin grup
│   ├── etc/           # Moderasi warn/kick/ban
│   └── tools/         # Kalkulator, QR, ID, Speedtest, dsb.
├── utils/             # Fungsi pendukung
├── setup.sh           # Auto-setup script
├── requirements.txt   # Dependensi Python
└── .env               # Token dan config privat
```

---

## 📈 Daftar Fitur (Perintah)

### 🚧 Admin Tools

* `/admins`, `/adminlist` — Cek admin grup
* `/promote`, `/demote`, `/sudo`
* `/clearchat`, `/purge`, `/kickme`
* `/lock`, `/rules`, `/welcome`
* `/tagall`, `/report`, `/log`
* `/watchlist`, `/activity`, `/insight`, `/joincleaner`

### ⛔️ Moderation Tools

* `/warn`, `/unwarn`, `/mute`, `/unmute`
* `/kick`, `/ban`, `/setwarnlimit`, `/setwarnaction`
* `/antilink`, `/antiflood`

### ⚖️ Utilities

* `/speedtest`, `/uptime`, `/afk`
* `/id`, `/userinfo`, `/groupinfo`
* `/calc`, `/qr`, `/quote`, `/source`
* `/broadcast`, `/github`

### 🧠 AI Tools *(jika diaktifkan)*

* `/ask <pertanyaan>` — AI tanya jawab
* `/image <prompt>` — AI image generator
* `/deepsearch` — AI-powered search

---

## 💡 Teknologi

* Python 3.10+
* Pyrogram
* SQLite (via `utils/database.py`)
* AI Integrations (optional): OpenRouter, Ollama, HuggingFace, Stability
* MongoDB Atlas (jika digunakan)

---

## 🔍 Contoh .env

```env
# Wajib
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here
USERNAME=your_bot_username_here

# Opsi AI
USE_AI=True
AI_PROVIDER=openrouter         # openrouter / ollama / hf / stability
OPENROUTER_API_KEY=your_openrouter_api_key
HF_API_TOKEN=your_huggingface_api_key
OLLAMA_MODEL=llama2
STABILITY_API_KEY=your_stability_ai_key

# Utilitas
SHRINKME_API_TOKEN=your_shrinkme_api_token
LINK_DONASI_SAWERIA=https://saweria.co/yourname

# Owner & Sudo
OWNER_ID=your_telegram_id
SUDO_USERS=123456789 987654321

# Database
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
```

---

## 🔧 Cara Mengakses Variabel ENV di Python

```python
from dotenv import load_dotenv
import os

load_dotenv(override=True)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("USERNAME")

USE_AI = os.getenv("USE_AI", "false").lower() == "true"
AI_PROVIDER = os.getenv("AI_PROVIDER")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

SHRINKME_API_TOKEN = os.getenv("SHRINKME_API_TOKEN")
LINK_DONASI_SAWERIA = os.getenv("LINK_DONASI_SAWERIA")

OWNER_ID = int(os.getenv("OWNER_ID"))
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split()))

MONGO_URI = os.getenv("MONGO_URI")
```

---

## 📆 Lisensi

Proyek ini berlisensi **MIT**. Bebas digunakan, dimodifikasi, dan didistribusikan dengan atribusi yang tepat.

---

<p align="center">Made with ❤️ by <a href="https://t.me/aesneverhere">@aesneverhere</a></p>
