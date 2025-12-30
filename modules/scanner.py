import subprocess
import os
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
        
        # Setting Mode Hybrid
        self.use_proxy_for_web = True  # Web tools lewat Tor
        self.use_proxy_for_nmap = False # Nmap lewat jalur direct (biar cepat)
        
        self.agent = AIAgent(provider, api_key)
        self.logger = EduLogger()
        self.tools_used = []
        
        domain = target_url.replace("https://", "").replace("http://", "").split("/")[0]
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_log_dir = f"logs/{domain}_{ts}"
        os.makedirs(self.session_log_dir, exist_ok=True)
        self.logger.set_log_dir(self.session_log_dir)

    def execute_command(self, command):
        final_cmd = command
        
        # Cek tool apa yang dipakai
        is_nmap = command.strip().lower().startswith("nmap")
        
        if is_nmap:
            if self.use_proxy_for_nmap:
                # Jika maksa Nmap lewat proxy (Lambat & Terbatas)
                final_cmd = f"proxychains -q {command}"
            else:
                # Nmap Direct (Cepat) + Decoy (Samarkan IP)
                # Kita inject flag Decoy jika belum ada
                if "-D" not in command:
                    # RND:5 artinya buat 5 IP palsu bareng IP asli kita
                    final_cmd = command.replace("nmap", "nmap -D RND:5")
        
        elif self.use_proxy_for_web:
            # Tool Web (Nuclei, Curl, etc) wajib lewat Tor
            final_cmd = f"proxychains -q {command}"
            
        try:
            # Timeout Nmap agak lama, tool web lewat proxy juga lama
            timeout_val = 600 
            process = subprocess.Popen(final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=timeout_val) 
            full = (stdout + stderr).strip()
            
            with open(f"{self.session_log_dir}/master_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\nCMD: {final_cmd}\n{full}\n{'='*40}\n")
                
            return full if full else "[No Output]"
        except Exception as e: return f"[ERROR]: {e}"

    def start_scan(self, max_steps=100):
        print(f"\033[1;32m[*] Scan Started. Logs: {self.session_log_dir}\033[0m")
        print(f"\033[1;36m[🛡️] HYBRID MODE ACTIVE:\033[0m")
        print(f"    ├── Nmap: Direct Connection (with Decoys) -> Fast")
        print(f"    └── Web : Proxychains (Tor) -> Anti-WAF")
        
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

        print("\n\033[1;33m[*] Scan Finished. Starting Reporter...\033[0m")
        Reporter(self.session_log_dir, self.target_url, self.provider, self.api_key).generate_report()