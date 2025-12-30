import subprocess
import os
import shutil
import time
from datetime import datetime
from modules.agent import AIAgent
from utils.reporter import Reporter
from utils.logger import EduLogger

class Scanner:
    def __init__(self, target_url, provider, api_key=None):
        self.target_url = target_url
        self.provider = provider
        self.api_key = api_key
        
        # Mode Hybrid
        self.use_proxy_for_web = True
        self.use_proxy_for_nmap = False
        
        self.agent = AIAgent(provider, api_key)
        self.logger = EduLogger()
        self.tools_used = []
        
        # --- LOGIC PEMBUATAN FOLDER KHUSUS ---
        # Membersihkan nama domain (hapus http, www, port, path)
        clean_domain = target_url.replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
        
        # Format Folder: logs/target.com_2025-12-30_10-00-00
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_log_dir = f"logs/{clean_domain}_{ts}"
        
        # Buat foldernya
        os.makedirs(self.session_log_dir, exist_ok=True)
        self.logger.set_log_dir(self.session_log_dir)

    def execute_command(self, command):
        final_cmd = command
        is_nmap = command.strip().lower().startswith("nmap")
        
        if is_nmap:
            if self.use_proxy_for_nmap:
                final_cmd = f"proxychains -q {command}"
            else:
                if "-D" not in command:
                    final_cmd = command.replace("nmap", "nmap -D RND:5")
        elif self.use_proxy_for_web:
            final_cmd = f"proxychains -q {command}"
            
        try:
            # Jalankan command
            process = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=600) 
            full = (stdout + stderr).strip()
            
            # Simpan log text ke folder khusus
            with open(f"{self.session_log_dir}/master_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\nCMD: {final_cmd}\n{full}\n{'='*40}\n")
                
            return full if full else "[No Output]"
        except Exception as e: return f"[ERROR]: {e}"

    # --- FITUR BARU: BERSIH-BERSIH FILE ---
    def cleanup_artifacts(self):
        print(f"\n\033[1;36m[🧹] Cleaning up workspace...\033[0m")
        # Daftar file sampah yang sering muncul di root
        common_files = ["index.html", "index.php", "robots.txt", "sitemap.xml", "wget-log"]
        
        # Pindahkan file-file ini ke dalam folder log sesi
        for filename in os.listdir("."):
            # Jika file ada di root DAN (termasuk daftar sampah ATAU file .html/.txt hasil download)
            if os.path.isfile(filename) and (filename in common_files or filename.endswith(".html") or filename.endswith(".log")):
                # Jangan pindahkan file sistem kita
                if filename in ["requirements.txt", "ferox.log"]: continue 
                
                try:
                    shutil.move(filename, os.path.join(self.session_log_dir, filename))
                    print(f"    └── Moved {filename} -> {self.session_log_dir}/")
                except: pass

    def start_scan(self, max_steps=100):
        print(f"\033[1;32m[*] Scan Started. Logs: {self.session_log_dir}\033[0m")
        print(f"\033[1;36m[🛡️] HYBRID MODE ACTIVE:\033[0m")
        print(f"    ├── Nmap: Direct Connection (with Decoys)")
        print(f"    └── Web : Proxychains (Tor)")
        
        curr = 1
        prev_out = None
        
        while curr <= max_steps:
            cmd = self.agent.decide_next_action(self.target_url, self.session_log_dir, prev_out, curr, ",".join(self.tools_used))
            tool = cmd.split(" ")[0].upper()
            if tool not in self.tools_used: self.tools_used.append(tool)
            
            self.logger.log(curr, f"AI executing {tool}", cmd)
            prev_out = self.execute_command(cmd)
            self.logger.log_output(prev_out)

            curr += 1
            time.sleep(1)

        # Panggil pembersih sebelum report
        self.cleanup_artifacts()

        print("\n\033[1;33m[*] Scan Finished. Starting Reporter...\033[0m")
        Reporter(self.session_log_dir, self.target_url, self.provider, self.api_key).generate_report()