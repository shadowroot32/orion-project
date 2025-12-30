# 🌌 ORION - AI Autonomous Red Team Framework
https://github.com/user-attachments/assets/bb33db37-dd8a-4e82-a303-5814043d5612

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Powered-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Orion** adalah kerangka kerja *Pentest Otonom* yang didukung oleh kecerdasan buatan (LLM). Alat ini mampu merencanakan, mengeksekusi, dan melaporkan celah keamanan secara mandiri menggunakan strategi *Cyber Kill Chain* (A-L).

Dirancang untuk **Kali Linux**, Orion menggabungkan kecepatan scanning manual dengan kecerdasan analisis AI.

---

## 🚀 Fitur Utama

### 🧠 1. Multi-Brain AI Support
Pilih otak AI yang ingin digunakan:
- **Groq (Llama3-70b):** Super cepat & Gratis.
- **Gemini (1.5 Flash):** Analisis mendalam & Gratis.
- **OpenAI (GPT-4o):** Akurasi tinggi (Berbayar).
- **Ollama (Local):** Privasi total (Offline).

### 🛡️ 2. Hybrid Stealth Mode (Anti-Ban)
Sistem pintar yang memisahkan jalur lalu lintas data:
- **Web Tools (Nuclei, Curl, Ferox):** Otomatis melalui **Tor Proxychains** (Rotasi IP) untuk menghindari WAF.
- **Network Tools (Nmap):** Koneksi Langsung + **Decoy IPs** (IP Palsu) agar tetap cepat namun tersamar.

### 📑 3. Professional AI Reporting
Bukan sekadar log mentah. Orion menghasilkan laporan setara konsultan keamanan:
- **Format:** PDF, HTML, dan Markdown.
- **Konten:** Ringkasan Eksekutif, Analisis Teknis, Dampak, dan Remediasi.
- **Bahasa:** Laporan otomatis dalam Bahasa Indonesia.

### ⚔️ 4. Full Kill Chain Arsenal
- **Recon:** Wafw00f, Whatweb, Whois.
- **Discovery:** Nuclei, Feroxbuster, Arjun.
- **Exploitation:** SQLMap, Hydra, Weevely.
- **Cloud:** AWS S3 Scanner, Cloud Enum.
- **PrivEsc:** LinPEAS (Linux Privilege Escalation).

---

## 📦 Instalasi

### Prasyarat (Kali Linux)
Install tool pendukung (Tor & Proxychains wajib untuk Hybrid Mode):
```bash
sudo apt update
sudo apt install -y tor proxychains4 python3-pip git nmap whatweb sqlmap hydra
```
## Setup Project
### 1. Clone Repository:
```bash
git clone [https://github.com/USERNAME-KAMU/orion-project.git](https://github.com/USERNAME-KAMU/orion-project.git)
cd orion-project
```
### 2. Install Python Libraries:
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi API Key: Buat file .env dan isi kunci API (pilih salah satu atau semua):
```bash
GROQ_API_KEY=gsk_xxxx
GEMINI_API_KEY=AIzaSyxxxx
OPENAI_API_KEY=sk-xxxx
```

### 4. Aktifkan Tor (Untuk Mode Stealth):
```bash
sudo service tor start
```
## 🎮 Cara Penggunaan
### 1. Jalankan script utama:
```bash
python main.py
```
## Menu Navigasi:
Pilih AI: Pilih otak yang akan mengendalikan serangan.

Input Target: Masukkan URL (contoh: http://testphp.vulnweb.com).

Pilih Mode Serangan:

Total War: Menjalankan seluruh arsenal dari Recon sampai Exploit.

Recon Only: Hanya mengumpulkan informasi pasif.

Discovery: Mencari celah spesifik (CVE/Bug).

Cloud: Scanning bucket S3.

Tentukan Langkah: Masukkan jumlah steps (Default: 100).

## 📂 Struktur Project
orion-project/
├── main.py              # Menu Utama
├── requirements.txt     # Dependencies
├── .env                 # API Keys (Jangan di-upload)
├── logs/                # Hasil Scan & Laporan PDF
├── modules/
│   ├── agent.py         # Otak Strategi (AI Logic)
│   └── scanner.py       # Eksekutor Perintah (Hybrid Mode)
└── utils/
    ├── ai_engine.py     # Konektor API (Groq/Gemini/dll)
    ├── logger.py        # Tampilan Terminal Cantik
    └── reporter.py      # Generator Laporan PDF/HTML
## ⚠️ Disclaimer
Alat ini dibuat HANYA UNTUK TUJUAN EDUKASI DAN PENGUJIAN KEAMANAN LEGAL.

Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.

Jangan gunakan pada target yang tidak Anda miliki izin tertulisnya.

Use at your own risk.

Happy Hacking! 🕵️‍♂️