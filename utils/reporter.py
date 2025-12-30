import os
import markdown
try:
    from weasyprint import HTML, CSS
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
from datetime import datetime
from utils.ai_engine import AIEngine
from colorama import Fore, Style, init

init(autoreset=True)

class Reporter:
    def __init__(self, log_dir, target, provider, api_key):
        self.log_dir = log_dir
        self.target = target
        self.engine = AIEngine(provider, api_key)
        self.base_report_path = os.path.join(log_dir, "PROFESSIONAL_REPORT")
        
        self.css_style = """
            @page { size: A4; margin: 2cm; }
            body { font-family: sans-serif; line-height: 1.6; color: #333; }
            h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; }
            h2 { color: #e67e22; border-bottom: 1px solid #eee; margin-top: 30px; }
            code { background: #f4f4f4; padding: 2px 5px; font-family: monospace; }
            pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; white-space: pre-wrap; }
        """

    def read_logs(self):
        combined = ""
        if not os.path.exists(self.log_dir): return ""
        for f in sorted(os.listdir(self.log_dir)):
            if f.endswith(".txt") and f != "master_log.txt":
                try:
                    path = os.path.join(self.log_dir, f)
                    content = open(path, "r", encoding="utf-8", errors="ignore").read().strip()
                    if content: combined += f"\n### Log: {f}\n```text\n{content[:2000]}...\n```\n"
                except: pass
        return combined

    def generate_report(self):
        print(f"\n{Fore.CYAN}[REPORT] Initializing AI Reporter...{Style.RESET_ALL}")
        evidence = self.read_logs()
        if not evidence: return print(f"{Fore.RED}[!] No logs found.{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}  └── Sending data to AI...{Style.RESET_ALL}")
        prompt = f"""
        Write a Professional Penetration Test Report in INDONESIAN.
        TARGET: {self.target}
        LOGS: {evidence}
        STRUCTURE:
        # Laporan Audit Keamanan
        ## 1. Ringkasan Eksekutif
        ## 2. Metodologi
        ## 3. Temuan Teknis & Dampak
        ## 4. Rekomendasi
        """

        try:
            md = self.engine.chat("You are a Security Auditor. Output Markdown.", prompt)
            
            with open(f"{self.base_report_path}.md", "w", encoding="utf-8") as f: f.write(md)
            print(f"{Fore.GREEN}  ├── Saved MD{Style.RESET_ALL}")

            html = f"<html><head><style>{self.css_style}</style></head><body>{markdown.markdown(md, extensions=['fenced_code', 'tables'])}</body></html>"
            with open(f"{self.base_report_path}.html", "w", encoding="utf-8") as f: f.write(html)
            print(f"{Fore.GREEN}  ├── Saved HTML{Style.RESET_ALL}")

            if PDF_SUPPORT:
                HTML(string=html).write_pdf(f"{self.base_report_path}.pdf")
                print(f"{Fore.GREEN}  └── Saved PDF{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}  └── PDF Skipped (Install weasyprint){Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[!] Report Failed: {e}{Style.RESET_ALL}")