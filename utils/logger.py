import sys
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class EduLogger:
    def __init__(self):
        self.log_file = None

    def set_log_dir(self, log_dir):
        self.log_file = os.path.join(log_dir, "master_log.txt")

    def log(self, step, description, technical_detail):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{Fore.YELLOW}┌── [STEP {step}] {timestamp} - {description}")
        print(f"{Fore.YELLOW}│")
        print(f"{Fore.GREEN}├── 🤖 Action  : {Fore.WHITE}{technical_detail}")
        print(f"{Fore.YELLOW}└───────────────────────────────────────────────{Style.RESET_ALL}")

        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] STEP {step}: {description}\nCMD: {technical_detail}\n{'-'*40}\n")
            except: pass

    def log_output(self, output_text):
        clean_out = output_text.strip()
        if not clean_out: return
        preview = clean_out[:200].replace("\n", " ")
        print(f"    {Fore.CYAN}└── [RESULT]: {Fore.WHITE}{preview}...")