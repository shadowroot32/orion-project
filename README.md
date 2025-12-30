# 🌌 ORION AUDIT FRAMEWORK

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-black?style=for-the-badge&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/AI-Hybrid%20Engine-purple?style=for-the-badge)

> **Advanced Autonomous AI Penetration Testing & Reporting Framework**

`![Screenshot Tool](path/to//home/sr01/Pictures/Screenshots/Screenshot_20251227_175617.png)`

**Orion** adalah kerangka kerja audit keamanan siber otomatis yang menggabungkan kecerdasan buatan (AI) dengan *arsenal* tools Kali Linux. Tidak sekadar *scanner* biasa, Orion bertindak sebagai **Agen Otonom** yang mampu berpikir, menganalisis output scan, dan menentukan langkah serangan selanjutnya secara logis.

---

## 🚀 Fitur Unggulan

* **🧠 Hybrid AI Engine:** Mendukung fleksibilitas penuh pemilihan "otak" AI:
    * **Groq (Llama 3.3):** Kecepatan super tinggi (Real-time).
    * **Google Gemini:** Analisis cerdas dan stabil.
    * **OpenAI (GPT-4o):** Standar industri.
    * **Ollama (Local):** Privasi penuh & berjalan offline.
* **🤖 Autonomous Logic:** AI menganalisis output (misal: port 80 terbuka) lalu otomatis memutuskan untuk menjalankan `nikto` atau `gobuster` tanpa campur tangan manusia.
* **🔥 Total War Mode:** Melakukan audit mendalam hingga **100 langkah** eksekusi tools secara beruntun.
* **📝 Triple-Format Reporting:** Menghasilkan laporan profesional dalam format **PDF, HTML, dan Markdown** secara otomatis.
* **🛡️ Kali Linux Native:** Terintegrasi langsung dengan tools seperti `Nmap`, `Sqlmap`, `Nikto`, `Wafw00f`, `Hydra`, dll.
* **⚡ CLI & Menu Mode:** Bisa dijalankan via menu interaktif atau *command line arguments* untuk otomatisasi cepat (`-y`).

---

## 🛠️ Instalasi & Persiapan

Ikuti langkah ini untuk mengatur lingkungan pengembangan yang bersih menggunakan **Virtual Environment**.

### 1. Prasyarat
Pastikan Anda menggunakan **Kali Linux** atau **Parrot OS** dan memiliki Python 3 terinstall.

### 2. Clone Repository
```bash
git clone [https://github.com/USERNAME-ANDA/orion-project.git](https://github.com/USERNAME-ANDA/orion-project.git)
cd orion-project
```

### 3. Setup Virtual Environment (Sangat Disarankan)
Gunakan virtual environment agar library project tidak mengganggu sistem Linux utama Anda.
```bash
# Install paket venv (jika belum ada)
sudo apt install python3-venv

# Buat virtual environment bernama 'myenv'
python3 -m venv myenv

# Aktifkan virtual environment
# (Tanda (myenv) akan muncul di terminal Anda)
source myenv/bin/activate
```

### 4. Install Dependencies
Install semua library Python yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 5. Install System Tools
Untuk fitur generate PDF laporan, kita membutuhkan wkhtmltopdf:
```bash
sudo apt update
sudo apt install wkhtmltopdf
```
## ⚙️ Konfigurasi API Key
Orion menggunakan file .env untuk menyimpan kunci rahasia agar aman dan tidak perlu diketik ulang.

### 1.Buat file .env di dalam folder project:
```bash
nano .env
```
### 2. Salin dan isi konfigurasi berikut (sesuaikan dengan AI yang ingin dipakai):
```bash
# Pilih salah satu atau isi semua (Opsional)
GROQ_API_KEY=gsk_yoursuperfastkey...
GEMINI_API_KEY=AIzaSyYourGoogleKey...
OPENAI_API_KEY=sk-proj-YourOpenAIKey...
```

### 3. Simpan file (Ctrl+O, Enter) dan keluar (Ctrl+X).

## 💻 Cara Penggunaan
Pastikan virtual environment aktif (source myenv/bin/activate) sebelum menjalankan program.

➤ Mode Menu Interaktif (Recommended)
Jalankan tanpa argumen untuk masuk ke menu navigasi visual. Anda bisa memilih AI, jumlah langkah, dan target.
```bash
python main.py
```
➤ Mode CLI (Cepat/Otomatis)
Gunakan argumen untuk bypass menu. Cocok untuk task cepat.
```bash
# Format: python main.py -y -t [TARGET] -s [STEPS]

# Contoh: Scan google.com, 50 langkah, auto-approve (tanpa tanya y/n)
python main.py -y -t google.com -s 50
```

### 📂 Struktur Project
```bash
orion-project/
├── modules/
│   ├── agent.py          # Otak AI (Prompt Engineering)
│   ├── backend.py        # Modul SQLi & Server
│   ├── frontend.py       # Modul XSS & Client
│   └── recon.py          # Modul Nmap & OSINT
├── utils/
│   ├── ai_engine.py      # Pengendali Multi-Provider (Groq/Gemini/dll)
│   ├── ai_reporter.py    # Generator PDF/HTML Report
│   └── kali_executor.py  # Eksekutor perintah Terminal
├── reports/              # Hasil laporan tersimpan di sini
├── .env                  # File API Key (RAHASIA)
├── .gitignore            # Filter upload Git
├── main.py               # Program Utama
└── requirements.txt      # Daftar Library
```

### ⚠️ Disclaimer
DISCLAIMER: > Alat ini dibuat semata-mata untuk Tujuan Edukasi dan Ethical Hacking (Audit Keamanan Resmi). Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini untuk menyerang target tanpa izin tertulis (illegal hacking). Gunakan dengan bijak dan bertanggung jawab.

### Developed with 💻 & ☕ by [ShadowRoot32]
