import subprocess
import os
import time
from datetime import datetime

# IMPORT DARI MODUL LAIN
from modules.agent import AIAgent

# IMPORT DARI UTILS (Sesuai Folder Anda)
from utils.reporter import Reporter
from utils.logger import EduLogger

class Scanner:
    def __init__(self, target_url, provider, api_key=None):
        self.target_url = target_url
        self.provider = provider
        self.api_key = api_key
        
        self.agent = AIAgent(provider, api_key)
        self.logger = EduLogger()
        self.tools_used = []
        
        domain = target_url.replace("https://", "").replace("http://", "").split("/")[0]
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_log_dir = f"logs/{domain}_{ts}"
        os.makedirs(self.session_log_dir, exist_ok=True)
        self.logger.set_log_dir(self.session_log_dir)

    def execute_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=300) 
            full = (stdout + stderr).strip()
            
            with open(f"{self.session_log_dir}/master_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\nCMD: {command}\n{full}\n{'='*40}\n")
                
            return full if full else "[No Output]"
        except Exception as e: return f"[ERROR]: {e}"

    def start_scan(self, max_steps=100):
        print(f"\033[1;32m[*] Scan Started. Logs: {self.session_log_dir}\033[0m")
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