import subprocess
import os
import shutil
import time
import sys
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
        
        # Setup Folder Log
        clean_domain = target_url.replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_log_dir = f"logs/{clean_domain}_{ts}"
        
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
            process = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=600) 
            full = (stdout + stderr).strip()
            
            with open(f"{self.session_log_dir}/master_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\nCMD: {final_cmd}\n{full}\n{'='*40}\n")
                
            return full if full else "[No Output]"
        except subprocess.TimeoutExpired:
            return "[ERROR] Command Timeout (Process Killed)"
        except Exception as e: 
            return f"[ERROR]: {e}"

    def cleanup_artifacts(self):
        print(f"\n\033[1;36m[🧹] Cleaning up artifacts...\033[0m")
        common_files = ["index.html", "index.php", "robots.txt", "sitemap.xml", "wget-log"]
        
        for filename in os.listdir("."):
            if os.path.isfile(filename) and (filename in common_files or filename.endswith(".html") or filename.endswith(".log") or filename.endswith(".php")):
                if filename in ["requirements.txt", "ferox.log", "main.py"]: continue 
                try:
                    shutil.move(filename, os.path.join(self.session_log_dir, filename))
                except: pass

    def start_scan(self, max_steps=100):
        print(f"\033[1;32m[*] Scan Started. Logs: {self.session_log_dir}\033[0m")
        print(f"\033[1;33m[!] Press Ctrl+C anytime to STOP and Generate Partial Report.\033[0m")
        
        curr = 1
        prev_out = None
        
        # --- BLOK UTAMA: TRY - EXCEPT - FINALLY ---
        try:
            while curr <= max_steps:
                print(f"\n\033[1;34m[STEP {curr}/{max_steps}] Thinking...\033[0m")
                
                # 1. AI Memutuskan
                cmd = self.agent.decide_next_action(self.target_url, self.session_log_dir, prev_out, curr, ",".join(self.tools_used))
                
                # Cek jika command kosong/error
                if not cmd: 
                    print("\033[1;31m[!] AI returned empty command. Skipping...\033[0m")
                    curr += 1
                    continue

                tool = cmd.split(" ")[0].upper()
                if tool not in self.tools_used: self.tools_used.append(tool)
                
                # 2. Eksekusi
                self.logger.log(curr, f"AI executing {tool}", cmd)
                prev_out = self.execute_command(cmd)
                self.logger.log_output(prev_out)

                curr += 1
                time.sleep(1)

        except KeyboardInterrupt:
            # Ini menangkap Ctrl+C
            print("\n\n\033[1;31m[!] SCAN INTERRUPTED BY USER (Ctrl+C)!\033[0m")
            print("\033[1;33m[*] Don't worry, saving collected data...\033[0m")
            
        except Exception as e:
            # Ini menangkap Error Program (Crash)
            print(f"\n\n\033[1;31m[!] CRITICAL ERROR OCCURRED: {e}\033[0m")
            print("\033[1;33m[*] Attempting to salvage report...\033[0m")

        finally:
            # --- BAGIAN INI SELALU DIJALANKAN ---
            # Baik sukses, stop manual, atau crash, kode di bawah ini PASTI jalan.
            
            print(f"\n\033[1;36m[🛡️] SAFE EXIT TRIGGERED\033[0m")
            
            # 1. Bersihkan file berceceran
            self.cleanup_artifacts()

            # 2. Generate Report dari apa yang ada
            print(f"\033[1;32m[*] Generating Report from available logs...\033[0m")
            try:
                reporter = Reporter(self.session_log_dir, self.target_url, self.provider, self.api_key)
                reporter.generate_report()
            except Exception as r_err:
                print(f"\033[1;31m[!] Report Generation Failed: {r_err}\033[0m")

            print(f"\n\033[1;37m[END] Session Closed. Logs: {self.session_log_dir}\033[0m")