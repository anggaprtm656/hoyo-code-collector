# 🎁 HoYo Codes Collector (All-in-One)

Database otomatis pengumpul kode promo aktif untuk 4 game HoYoverse:
- ⚔️ **Genshin Impact**
- 🚀 **Honkai: Star Rail**
- 📼 **Zenless Zone Zero**
- 💥 **Honkai Impact 3rd**

Diperbarui secara otomatis setiap **2 jam** menggunakan **GitHub Actions** langsung dari database komunitas Fandom Wiki.

---

## 📡 Endpoint JSON Langsung (Raw URL)

Gunakan tautan di bawah ini di aplikasi, bot Discord, atau skrip otomatis kamu:

| Game | Endpoint JSON Langsung |
| :--- | :--- |
| **Semua Game (All Active)** | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/active_codes.json` |
| **Genshin Impact** | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/active_genshin.json` |
| **Honkai: Star Rail** | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/active_hsr.json` |
| **Zenless Zone Zero** | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/active_zzz.json` |
| **Honkai Impact 3rd** | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/active_hi3.json` |

---

## 📄 Endpoint Plain Text (.txt) — Siap Copas & Script

Jika kamu butuh daftar kode mentah (1 kode per baris) tanpa format JSON:

| Game | File TXT | Link Raw TXT |
| :--- | :--- | :--- |
| **Semua Game** | `code/all.txt` | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/code/all.txt` |
| **Genshin Impact** | `code/genshin.txt` | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/code/genshin.txt` |
| **Honkai: Star Rail** | `code/hsr.txt` | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/code/hsr.txt` |
| **Zenless Zone Zero** | `code/zzz.txt` | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/code/zzz.txt` |
| **Honkai Impact 3rd** | `code/hi3.txt` | `https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/code/hi3.txt` |

---

## 🗄️ Arsip Kode Per Tahun

Agar data tidak menumpuk, semua kode yang pernah tercatat diarsipkan rapi per tahun di folder `data/archive/`:
- `data/archive/2026.json`
- `data/archive/2025.json`
- *(akan otomatis membuat tahun baru saat pergantian tahun)*

---

## 🚀 Cara Menjalankan Sendiri

1. **Jalankan Skrip Lokal:**
   ```bash
   python collector.py
   ```
2. **Otomatisasi:**
   Workflow GitHub Actions (`.github/workflows/auto_collector.yml`) akan otomatis berjalan setiap 2 jam dan memperbarui file JSON jika ada kode baru.
