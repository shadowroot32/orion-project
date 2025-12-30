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
        
        # --- UPDATE: Daftar file yang boleh dibaca AI ---
        allowed_ext = (".txt", ".log", ".html", ".xml", ".json", ".php", ".js", ".md")
        
        print(f"{Fore.CYAN}[REPORT] Reading artifacts from logs...{Style.RESET_ALL}")
        
        for f in sorted(os.listdir(self.log_dir)):
            # Cek apakah ekstensinya diizinkan
            if f.endswith(allowed_ext) and f != "master_log.txt":
                try:
                    path = os.path.join(self.log_dir, f)
                    # Baca file (ignore error jika ada karakter aneh)
                    content = open(path, "r", encoding="utf-8", errors="ignore").read().strip()
                    
                    if content:
                        # Batasi 3000 karakter per file agar AI tidak pusing/overload
                        preview = content[:3000]
                        combined += f"\n### File Evidence: {f}\n```text\n{preview}\n...(truncated)\n```\n"
                        print(f"  ├── Loaded: {f}")
                except Exception as e:
                    print(f"  ├── Error reading {f}: {e}")
                    
        return combined

    def generate_report(self):
        print(f"\n{Fore.CYAN}[REPORT] Initializing AI Reporter...{Style.RESET_ALL}")
        evidence = self.read_logs()
        if not evidence: return print(f"{Fore.RED}[!] No readable logs found.{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}  └── Sending data to AI (Thinking)...{Style.RESET_ALL}")
        prompt = f"""
        Write a Professional Penetration Test Report in INDONESIAN.
        TARGET: {self.target}
        EVIDENCE DATA:
        {evidence}
        
        INSTRUCTIONS:
        1. Analyze the 'File Evidence' above. If you see source code (HTML/JS), analyze it for secrets/comments.
        2. If you see tool logs (Nuclei/Nmap), summarize the findings.
        3. Structure the report formally.
        
        STRUCTURE:
        # Laporan Audit Keamanan: {self.target}
        ## 1. Ringkasan Eksekutif
        ## 2. Metodologi
        ## 3. Analisis Temuan (Technical Analysis)
        ## 4. Rekomendasi Perbaikan
        """

        try:
            md = self.engine.chat("You are a Senior Security Auditor. Output Markdown only.", prompt)
            
            # Simpan Markdown
            with open(f"{self.base_report_path}.md", "w", encoding="utf-8") as f: f.write(md)
            print(f"{Fore.GREEN}  ├── Saved MD Report{Style.RESET_ALL}")

            # Convert ke HTML
            html = f"<html><head><style>{self.css_style}</style></head><body>{markdown.markdown(md, extensions=['fenced_code', 'tables'])}</body></html>"
            with open(f"{self.base_report_path}.html", "w", encoding="utf-8") as f: f.write(html)
            print(f"{Fore.GREEN}  ├── Saved HTML Report{Style.RESET_ALL}")

            # Convert ke PDF
            if PDF_SUPPORT:
                try:
                    HTML(string=html).write_pdf(f"{self.base_report_path}.pdf")
                    print(f"{Fore.GREEN}  └── Saved PDF Report{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}  └── PDF Error: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}  └── PDF Skipped (Install weasyprint){Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[!] Report Failed: {e}{Style.RESET_ALL}")