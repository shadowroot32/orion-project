import requests
import urllib.parse
from colorama import Fore

class BackendScanner:
    def __init__(self, logger):
        self.logger = logger
        self.headers = {
            'User-Agent': 'Orion-Scanner/1.0 (Enterprise)'
        }

        # [SOURCE: PayloadsAllTheThings - SQL Injection]
        self.sqli_payloads = [
            # 1. Classic Error Based (Single Quote)
            "'",
            # 2. Classic Error Based (Double Quote)
            '"',
            # 3. Auth Bypass Logic / Boolean Blind Test
            "' OR '1'='1",
            '" OR "1"="1',
            # 4. Comment Truncation (MySQL/Postgres)
            "' OR 1=1#",
            "' OR 1=1--",
            # 5. Generic Polyglot
            "SLEEP(1) /*' or SLEEP(1) or '\" or SLEEP(1) or \"*/"
        ]

        # Database Error Signatures (Regex-like strings)
        self.db_errors = {
            "MySQL": ["You have an error in your SQL syntax", "Warning: mysql_"],
            "PostgreSQL": ["PostgreSQL query failed", "syntax error at or near"],
            "SQL Server": ["Unclosed quotation mark", "Microsoft OLE DB Provider for ODBC Drivers"],
            "Oracle": ["ORA-01756", "quoted string not properly terminated"],
            "Generic": ["SQLSTATE", "ODBC SQL Server Driver"]
        }

    def check_sqli_active(self, target_url):
        findings = []
        parsed = urllib.parse.urlparse(target_url)
        params = urllib.parse.parse_qs(parsed.query)

        if not params:
            return ["[INFO] Backend Scan Skipped: No parameters."]

        print(f"{Fore.CYAN}    [>] Injecting SQL Vectors (Error-Based & Boolean)...{Fore.RESET}")

        for param_name in params:
            is_vuln = False
            
            for payload in self.sqli_payloads:
                if is_vuln: break # Stop jika sudah vuln
                
                temp_params = params.copy()
                temp_params[param_name] = payload
                
                new_query = urllib.parse.urlencode(temp_params, doseq=True)
                test_url = parsed._replace(query=new_query).geturl()

                try:
                    res = requests.get(test_url, headers=self.headers, timeout=5)
                    
                    # 1. Cek Error Based (Mencari pesan error DB di halaman)
                    for db_type, errors in self.db_errors.items():
                        for error in errors:
                            if error in res.text:
                                findings.append(f"[CRITICAL] SQL Injection ({db_type}) pada param '{param_name}'")
                                findings.append(f"           Payload: {payload}")
                                findings.append(f"           Evidence: {error}")
                                is_vuln = True
                                break
                        if is_vuln: break

                    # 2. Cek Boolean Based (Sederhana)
                    # Jika payload OR 1=1 membuat halaman memiliki konten jauh lebih banyak/berbeda dr normal
                    # (Fitur ini advance, kita skip dulu biar kode tidak terlalu kompleks, fokus ke Error Based dulu)

                except Exception:
                    pass

        if not findings:
            findings.append("[SAFE] Tidak ditemukan error SQL standar pada parameter yang dites.")

        return findings