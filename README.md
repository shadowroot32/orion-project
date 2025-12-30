# 🌌 ORION: AI-Powered Autonomous Red Team Framework
<img width="484" height="525" alt="Image" src="https://github.com/user-attachments/assets/74ded6a9-13f4-4dcf-b37a-01c4c3d99583" />


![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI-Powered](https://img.shields.io/badge/AI-Gemini%20%7C%20Groq%20%7C%20Ollama-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-red)

**Orion** is an autonomous penetration testing framework driven by Large Language Models (LLMs). Unlike traditional scanners that randomly fire scripts, Orion **"thinks"** like a human hacker. It analyzes output, decides the next best move, and executes a full Cyber Kill Chain from Reconnaissance to Covering Tracks.

> ⚠️ **DISCLAIMER:** This tool is for **EDUCATIONAL PURPOSES & AUTHORIZED PENTESTING ONLY**. The author is not responsible for any misuse.

---

## 🧠 Why Orion?

- **🤖 AI Brain:** Uses Google Gemini, Groq, or Ollama to analyze vulnerabilities in real-time.
- **💸 Token Saver Engine:** Automatically filters "junk logs" (progress bars, banners) to reduce API costs by 80%.
- **🔄 Anti-Loop Logic:** Detects if a tool is stuck and forces a strategy shift.
- **☁️ Hybrid Cloud Hunting:** If the web server is secure, Orion pivots to find exposed AWS S3 buckets or Azure Blobs.
- **🏴‍☠️ Full Kill Chain:** Covers strategies A through L (see below).

---

## 🗺️ The Strategy: Kill Chain A-L

Orion follows a strict military-grade attack framework:

| Strategy | Code | Description | Tools Used |
| :--- | :---: | :--- | :--- |
| **Recon** | `A` | WAF detection & Tech fingerprinting | `wafw00f`, `whatweb` |
| **Discovery** | `B` | Vulnerability scanning & Fuzzing | `nuclei`, `feroxbuster` |
| **Guerrilla** | `G` | Hidden parameter hunting | `arjun` |
| **Exploitation** | `C` | Database injection & Brute-force | `sqlmap`, `hydra` |
| **Weaponization**| `E` | Backdoor/Payload generation | `weevely`, `msfvenom` |
| **Looting** | `F` | Stealing Source Code & Secrets | `git-dumper`, `curl` |
| **Cloud** | `H` | S3 Bucket Enumeration | `cloud_enum`, `awscli` |
| **Internal** | `I` | Internal Network Mapping | `nmap`, `ping` |
| **PrivEsc** | `K` | Privilege Escalation (Root) | `linpeas`, `suid` |
| **Laundering** | `L` | Log Wiping & cleanup | `rm`, `history -c` |

---

## 🛠️ Installation

Orion requires **Kali Linux** or a similar Debian-based pentest distro.

### 1. System Dependencies
Install core tools from the Kali repository:
```bash
sudo apt update && sudo apt install -y \
    python3-pip python3-venv \
    nmap wafw00f whatweb nuclei feroxbuster \
    arjun sqlmap hydra weevely awscli \
    curl wget git

### 2. Manual Install: Cloud Enum (Important!)
Since cloud_enum is not in standard repositories, install it manually:
```bash
# Clone to /opt
sudo git clone [https://github.com/initstring/cloud_enum.git](https://github.com/initstring/cloud_enum.git) /opt/cloud_enum

# Setup Virtual Environment (to bypass PEP 668)
cd /opt/cloud_enum
sudo python3 -m venv venv
sudo ./venv/bin/pip install -r requirements.txt

# Create a Launcher Shortcut
echo '#!/bin/bash' | sudo tee /usr/bin/cloud_enum
echo '/opt/cloud_enum/venv/bin/python3 /opt/cloud_enum/cloud_enum.py "$@"' | sudo tee -a /usr/bin/cloud_enum
sudo chmod +x /usr/bin/cloud_enum
```

## 🚀 Usage

### 1. Clone the Repository:
```bash
# 1. clone repo
git clone [https://github.com/ShadowRoot32/orion-project.git](https://github.com/ShadowRoot32/orion-project.git)
cd orion-project

# 2. Create Virtual Environment
python3 -m venv venv

# 3. Activate Environment
source venv/bin/activate

# 4. Install Dependencies
pip install -r requirements.txt
pip install git-dumper
```
### 2. Setup API Keys: Create a .env file:
```bash
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
```
### 3. Run Orion:
```bash
python main.py
```
### 4. Select AI Provider:

Groq: Super fast (Recommended for short scans).

Gemini 1.5 Flash: Massive context window (Best for complex logs).

OpenAI 4.0 : Pay/Paid

Ollama: Offline & Uncensored (Requires local RAM).

## 📂 Project Structure
```bash
orion-project/
├── main.py              # Entry point (Menu System)
├── requirements.txt     # Python libs
├── .env                 # API Keys
├── modules/
│   ├── agent.py         # The AI Brain (Logic A-L)
│   └── scanner.py       # Tool execution wrapper
├── utils/
│   └── ai_engine.py     # API Handlers (Groq/Gemini/Ollama)
└── logs/                # All scan results saved here
```

## 🔮 Roadmap
[x] Integrate Cloud Hunting (AWS/Azure)

[x] Implement Token Saver (Compression)

[x] Add Anti-Loop Logic

[ ] Add Report Generator (PDF/HTML)

[ ] Add Telegram/Discord Notification

### ⚠️ Disclaimer
DISCLAIMER: > Alat ini dibuat semata-mata untuk Tujuan Edukasi dan Ethical Hacking (Audit Keamanan Resmi). Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini untuk menyerang target tanpa izin tertulis (illegal hacking). Gunakan dengan bijak dan bertanggung jawab.

### Developed with 💻 & ☕ by [ShadowRoot32]
