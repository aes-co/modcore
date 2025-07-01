# 🛡️ Security Policy for ModCore

## Supported Versions

Kami mendukung versi ModCore terbaru (branch `main`) dan hanya menerima laporan keamanan untuk versi ini.

| Version  | Supported |
| -------- | --------- |
| latest   | ✅         |
| \<latest | ❌         |

---

## 🚨 Melaporkan Kerentanan

Jika Anda menemukan bug atau potensi celah keamanan di proyek ini:

* Jangan laporkan secara publik.
* Kirim email ke: **[aesneverhere@pm.me](mailto:aesh.n@outlook.com)**
* Subjek: `[SECURITY] ModCore - <judul singkat>`
* Sertakan detail:

  * Langkah reproduksi
  * Lingkungan (Python version, OS)
  * Potensi dampak

Kami akan membalas dalam waktu 48 jam. Jika bug valid, kami akan:

* Merilis patch
* Mencantumkan Anda (jika ingin) dalam `SECURITY-ACK.md`

---

## 🔒 Praktik Keamanan

ModCore menerapkan beberapa praktik keamanan penting:

* `.env` digunakan untuk menyimpan token dan kredensial, **jangan pernah commit ke repo**.
* Plugin dinamis diproses dengan try-catch terkontrol.
* Logging sensitif disaring secara lokal (tidak log token/user).
* Kunci API hanya digunakan pada sisi server bot.
* Validasi input dilakukan untuk perintah user.

---

## 📝 Tips untuk Developer

* Gunakan `.env.sample` sebagai referensi, jangan bagikan `.env` asli.
* Tambahkan `.env`, `bot.log`, dan `__pycache__/` ke `.gitignore`.
* Jangan gunakan token asli saat uji publik / deploy ke Heroku / Railway.
* Pastikan dependency Anda up-to-date (lihat `requirements.txt`).

---

## 💬 Kontak

Jika Anda memiliki pertanyaan seputar keamanan proyek ini, silakan hubungi:

* Telegram: [@aesneverhere](https://t.me/aesneverhere)
* Email: **[aesneverhere@pm.me](mailto:aesh.n@outlook.com)**

---

Terima kasih telah membantu menjaga keamanan komunitas ModCore ❤️
