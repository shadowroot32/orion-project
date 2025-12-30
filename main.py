print("[-] [SYSTEM] Memulai Python Interpreter...") # Debug Print 1

import sys
import os
import argparse
import time

# Cek Library Dasar
try:
    from colorama import Fore, Style, init
    from dotenv import load_dotenv
    print("[-] [SYSTEM] Library dasar (Colorama/Dotenv) OK.") # Debug Print 2
except ImportError as e:
    print(f"[!] CRITICAL ERROR: Library hilang. Jalankan: pip install colorama python-dotenv")
    print(f"[!] Detail: {e}")
    sys.exit()

# Cek Modul Project
try:
    # Memastikan Python bisa membaca folder utils/modules
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from utils.ai_reporter import AIPentestReporter
    from modules.agent import AIAgent
    from utils.kali_executor import KaliExecutor
    print("[-] [SYSTEM] Modul internal (Agent/Executor) OK.") # Debug Print 3
except ImportError as e:
    print(f"[!] CRITICAL ERROR: Gagal memuat modul internal.")
    print(f"[!] Pastikan struktur folder benar (ada folder 'utils' dan 'modules').")
    print(f"[!] Detail: {e}")
    sys.exit()

load_dotenv()
init(autoreset=True)
VERSION = "7.2.0 (Stable Fix)"

# --- HELPER FUNCTIONS ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    # Menggunakan Raw String (r''') agar tidak error SyntaxWarning escape sequence
    print(r'''
    _  _  ____  ____  __  __  ____ 
   / )( \(  __)(_  _)(  )(  )(  _ \
   ) \/ ( ) _)   )(   )(__)(  ) __/
   \____/(__)   (__) (______)(__)  
                                
    ''' + f"{Fore.WHITE}ORION FRAMEWORK {Fore.GREEN}{VERSION}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Advanced Autonomous AI Pentesting{Style.RESET_ALL}\n")

def get_provider_choice():
    while True:
        print_banner()
        print(f"{Fore.YELLOW}[ MENU UTAMA ] PILIH AI ENGINE:{Style.RESET_ALL}")
        print("1. Groq (Llama 3.3)   --> [Super Cepat & Gratis]")
        print("2. Google Gemini      --> [Cerdas & Stabil]")
        print("3. OpenAI (GPT-4o)    --> [Berbayar]")
        print("4. Ollama (Local)     --> [Offline]")
        print(f"{Fore.RED}0. Exit               --> [Keluar]{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}[?] Masukkan Pilihan (0-4): {Style.RESET_ALL}").strip()
        
        if choice == '1': return "groq"
        elif choice == '2': return "gemini"
        elif choice == '3': return "openai"
        elif choice == '4': return "ollama"
        elif choice == '0': 
            print("Bye!"); sys.exit()
        else: 
            input(f"{Fore.RED}[!] Pilihan tidak valid. Tekan Enter...{Style.RESET_ALL}")

def get_step_config():
    while True:
        print(f"\n{Fore.YELLOW}[ CONFIG ] KEDALAMAN AUDIT:{Style.RESET_ALL}")
        print("1. Quick Scan       (10 Steps)")
        print("2. Standard Audit   (30 Steps)")
        print(f"{Fore.RED}3. TOTAL WAR        (100 Steps){Style.RESET_ALL}")
        print("4. Custom Jumlah")
        print(f"{Fore.BLUE}9. Back (Ganti AI){Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}[?] Pilihan: {Style.RESET_ALL}").strip()

        if choice == '1': return 10
        elif choice == '2': return 30
        elif choice == '3': return 100
        elif choice == '4':
            try: return int(input("Masukkan angka: "))
            except: pass
        elif choice == '9': return "BACK"

def get_target_input():
    while True:
        print(f"\n{Fore.YELLOW}[ TARGET ] MASUKKAN URL/IP:{Style.RESET_ALL}")
        print(f"(Ketik {Fore.BLUE}'back'{Style.RESET_ALL} kembali, {Fore.RED}'exit'{Style.RESET_ALL} keluar)")
        target = input(f"{Fore.GREEN}[?] Target: {Style.RESET_ALL}").strip()
        
        if target.lower() == 'back': return "BACK"
        if target.lower() == 'exit': sys.exit()
        if target: return target

# --- MAIN LOGIC ---
def main():
    print("[-] [SYSTEM] Masuk ke fungsi main()...") # Debug Print 4
    
    # CLI Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yes', action='store_true', help='Auto-Approve')
    parser.add_argument('-t', '--target', type=str, help='Target URL')
    parser.add_argument('-s', '--steps', type=int, help='Steps count')
    args = parser.parse_args()

    cli_mode = bool(args.target)

    while True:
        # 1. Pilih Provider
        if cli_mode:
            provider = "groq"
            print(f"{Fore.MAGENTA}[CLI] Default: GROQ{Style.RESET_ALL}")
        else:
            provider = get_provider_choice()

        # 2. Setup API Key
        api_key = None
        if provider != "ollama":
            env_var = f"{provider.upper()}_API_KEY"
            api_key = os.getenv(env_var)
            if not api_key:
                print(f"\n{Fore.YELLOW}[!] API Key {provider.upper()} tidak ada di .env{Style.RESET_ALL}")
                inp = input(f"{Fore.GREEN}[?] Masukkan Key Manual (atau 'back'): {Style.RESET_ALL}").strip()
                if inp.lower() == 'back': continue
                api_key = inp

        # 3. Pilih Steps
        while True:
            if cli_mode:
                max_steps = args.steps if args.steps else 50
            else:
                s = get_step_config()
                if s == "BACK": break
                max_steps = s

            # 4. Input Target
            while True:
                if cli_mode:
                    target = args.target
                else:
                    target = get_target_input()
                    if target == "BACK": break

                # --- START SESSION ---
                try:
                    print_banner()
                    print(f"{Fore.MAGENTA}[*] INISIALISASI AGENT...{Style.RESET_ALL}")
                    
                    executor = KaliExecutor(auto_approve=args.yes)
                    agent = AIAgent(provider, api_key)
                    reporter = AIPentestReporter(provider, api_key)

                    print(f"    Target : {target}")
                    print(f"    Engine : {provider.upper()}")
                    print("-" * 40)

                    history = []
                    last_out = None
                    used_tools = []
                    
                    # LOOP STEP
                    for i in range(1, max_steps + 1):
                        print(f"\n{Fore.CYAN}┌── [STEP {i}/{max_steps}] AI Thinking...{Style.RESET_ALL}")
                        
                        ctx = ", ".join(used_tools[-10:])
                        cmd = agent.decide_next_action(target, last_out, i, ctx)
                        
                        # Simpan tool yg dipakai
                        tname = cmd.split(" ")[0]
                        if tname not in used_tools: used_tools.append(tname)

                        if "FINISH" in cmd:
                            print(f"{Fore.GREEN}└── AI Selesai.{Style.RESET_ALL}")
                            break
                        
                        print(f"{Fore.YELLOW}└── Command: {cmd}{Style.RESET_ALL}")
                        
                        out = executor.run_command(cmd)
                        
                        if "skipped" in out:
                            print(f"{Fore.RED}[!] Dibatalkan user.{Style.RESET_ALL}")
                            break
                        
                        print(f"{Fore.BLUE}    [OUTPUT]: {len(out)} chars.{Style.RESET_ALL}")
                        history.append({"step": i, "command": cmd, "output": out})
                        last_out = out

                    # REPORTING
                    if history:
                        print(f"\n{Fore.MAGENTA}┌── MEMBUAT LAPORAN...{Style.RESET_ALL}")
                        files = reporter.generate_agent_report(target, history)
                        print(f"\n{Fore.GREEN}[SUCCESS] Laporan tersimpan!{Style.RESET_ALL}")
                        print(f"Files: {files}")
                    
                    input(f"\n{Fore.GREEN}[Tekan Enter kembali ke menu]{Style.RESET_ALL}")
                    if cli_mode: sys.exit()
                    break

                except KeyboardInterrupt:
                    print(f"\n{Fore.RED}[!] Force Stop.{Style.RESET_ALL}")
                    sys.exit()
                except Exception as e:
                    print(f"\n{Fore.RED}[CRASH ERROR] {e}{Style.RESET_ALL}")
                    import traceback
                    traceback.print_exc() # Print detail error
                    input("Tekan Enter...")
                    sys.exit()

            if target == "BACK": continue
            else: break
        if provider == "BACK": continue

# --- PENTING: ENTRY POINT ---
# Jika bagian ini hilang, script tidak akan jalan
if __name__ == "__main__":
    main()