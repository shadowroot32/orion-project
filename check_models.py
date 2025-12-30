import os
from colorama import Fore, Style, init
# [FIX] Import baru
from google import genai 
from groq import Groq
from openai import OpenAI
import ollama

init(autoreset=True)

def check_gemini():
    print(f"\n{Fore.CYAN}=== GOOGLE GEMINI ==={Style.RESET_ALL}")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{Fore.RED}[SKIP] API Key not found.{Style.RESET_ALL}")
        return

    try:
        # [FIX] Client Baru
        client = genai.Client(api_key=api_key)
        print(f"{Fore.GREEN}[SUCCESS] Gemini Connected. Listing Models:{Style.RESET_ALL}")
        # [FIX] Cara list model baru
        for m in client.models.list():
            print(f"  - {m.name}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

# ... (Kode Groq, OpenAI, Ollama lainnya tetap sama) ...

if __name__ == "__main__":
    check_gemini()
    # Panggil fungsi cek lainnya jika perlu