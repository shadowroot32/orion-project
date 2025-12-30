import subprocess
import sys
from colorama import Fore

class KaliExecutor:
    def __init__(self, auto_approve=False):
        """
        Inisialisasi Executor.
        :param auto_approve: Jika True, lewati konfirmasi user (mode -y).
        """
        self.auto_approve = auto_approve

    def run_command(self, command):
        print(f"{Fore.YELLOW}[AGENT] Executing: {command}{Fore.RESET}")
        
        # --- LOGIKA SMART CONFIRMATION ---
        if self.auto_approve:
            # Jika mode -y aktif, langsung gas
            print(f"{Fore.CYAN}    └── [AUTO -y] Perintah disetujui otomatis.{Fore.RESET}")
        else:
            # Jika tidak, tanya user dulu (Default)
            try:
                confirm = input(f"{Fore.CYAN}    └── Izinkan perintah ini? (y/n): {Fore.RESET}")
                if confirm.lower() != 'y':
                    return "Command execution skipped by user."
            except KeyboardInterrupt:
                return "skipped"

        # --- EKSEKUSI ---
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if result.returncode == 0:
                output = result.stdout
                return output[:8000] 
            else:
                return f"Error executing tool: {result.stderr}"
                
        except Exception as e:
            return f"System Error: {str(e)}"