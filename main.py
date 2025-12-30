import os
import sys
import time
from dotenv import load_dotenv
from modules.scanner import Scanner

# Load Environment Variables
load_dotenv()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# --- INI BAGIAN YANG KITA KEMBALIKAN ---
def print_banner():
    print("""\033[1;36m
      ██████╗ ██████╗ ██╗ ██████╗ ███╗   ██╗
     ██╔═══██╗██╔══██╗██║██╔═══██╗████╗  ██║
     ██║   ██║██████╔╝██║██║   ██║██╔██╗ ██║
     ██║   ██║██╔══██╗██║██║   ██║██║╚██╗██║
     ╚██████╔╝██║  ██║██║╚██████╔╝██║ ╚████║
      ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
     \033[1;33m[ AI AUTONOMOUS RED TEAM FRAMEWORK ]\033[0m
    """)

def get_custom_steps(default_val):
    try:
        user_input = input(f"\n\033[1;34m[?] Enter Max Steps (Default {default_val}): \033[0m").strip()
        if not user_input: return default_val
        val = int(user_input)
        return val if val > 0 else default_val
    except: return default_val

def main_menu():
    while True:
        clear_screen()
        print_banner() # <--- Memanggil banner besar
        
        print("\033[1;34m[ SELECT AI BRAIN ]\033[0m")
        print("1. Groq (Llama3-70b)     - \033[92mFast & Free\033[0m")
        print("2. Gemini (1.5 Flash)    - \033[92mSmart & Free\033[0m")
        print("3. Ollama (Local)        - \033[93mOffline & Privacy\033[0m")
        print("4. OpenAI (GPT-4o)       - \033[91mPaid & Smarter\033[0m")
        print("-" * 30)
        print("0. \033[1;31mEXIT PROGRAM\033[0m")
        
        c = input("\nChoice [0-4]: ").strip()
        if c == '0': sys.exit(0)
        
        prov, key = "", ""
        if c == '1': prov, key = "groq", os.getenv("GROQ_API_KEY")
        elif c == '2': prov, key = "gemini", os.getenv("GEMINI_API_KEY")
        elif c == '3': prov = "ollama"
        elif c == '4': prov, key = "openai", os.getenv("OPENAI_API_KEY")
        else: continue
        
        # Cek Key (Kecuali Ollama)
        if prov != "ollama" and not key:
            print(f"\n\033[1;31m[!] ERROR: API Key for {prov.upper()} not found in .env!\033[0m")
            time.sleep(2)
            continue
        
        target_menu(prov, key)

def target_menu(provider, api_key):
    while True:
        clear_screen()
        print_banner()
        print(f"\033[1;33m[ ACTIVE BRAIN: {provider.upper()} ]\033[0m")
        
        target = input("\n\033[1;32m[?] Enter Target URL (or '9' Back): \033[0m").strip()
        if target == '9': return
        if not target: continue
        
        attack_mode_menu(provider, api_key, target)

def attack_mode_menu(provider, api_key, target):
    while True:
        clear_screen()
        print_banner()
        print(f"Target: \033[1;32m{target}\033[0m | AI: \033[1;33m{provider.upper()}\033[0m")
        print("\n\033[1;35m[ SELECT STRATEGY ]\033[0m")
        print("1. \033[1;31mTOTAL WAR (A-L)\033[0m   - Full Kill Chain")
        print("2. \033[1;36mRECONNAISSANCE\033[0m    - Passive Intel")
        print("3. \033[1;33mDISCOVERY\033[0m         - Find Bugs")
        print("4. \033[1;31mEXPLOITATION\033[0m      - Get Shell")
        print("5. \033[1;37mCLOUD HUNTING\033[0m     - AWS S3")
        print("-" * 30)
        print("9. \033[1;33mBACK\033[0m")
        print("0. \033[1;31mEXIT\033[0m")
        
        c = input("\nChoice [0-9]: ").strip()
        if c == '9': return 
        if c == '0': sys.exit(0)

        mode, steps = "ALL", 100
        if c == '2': mode, steps = "RECON", 15
        elif c == '3': mode, steps = "DISCOVERY", 30
        elif c == '4': mode, steps = "EXPLOIT", 50
        elif c == '5': mode, steps = "CLOUD", 20
        elif c != '1': continue

        final_steps = get_custom_steps(steps)

        print(f"\n\033[1;33m[*] Initializing Orion Agent...\033[0m")
        time.sleep(1)
        
        try:
            # Panggil Scanner
            scanner = Scanner(target_url=target, provider=provider, api_key=api_key)
            scanner.agent.set_mode(mode)
            scanner.start_scan(max_steps=final_steps)
            
            input("\n\033[1;32m[+] Mission Complete. Press Enter to return...\033[0m")
        except KeyboardInterrupt:
            return 
        except Exception as e:
            print(f"\n\033[1;31m[!] Critical Error: {e}\033[0m")
            input("Press Enter...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(0)