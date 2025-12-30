import random
import re
from urllib.parse import urlparse
from utils.ai_engine import AIEngine

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)
        self.mode = "ALL"
        
        # --- ARSENAL ---
        self.web_arsenal = [
            "nmap", "whatweb", "wafw00f", 
            "nuclei", "feroxbuster", "arjun", 
            "sqlmap", "hydra", "weevely", 
            "curl", "wget", "git-dumper"
        ]
        
        self.infra_arsenal = [
            "nmap", "masscan", "whois", 
            "hydra", "netcat", "ping" 
        ]
        
        self.tool_sequence = self.web_arsenal

    def auto_detect_scope(self, target_input):
        if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", target_input):
            self.tool_sequence = self.infra_arsenal
            return "INFRA (IP Address)"
        self.tool_sequence = self.web_arsenal
        return "DOMAIN ASSET (Web/Other)"

    def set_mode(self, mode_name):
        self.mode = mode_name.upper()
        if self.mode == "RECON": 
            self.tool_sequence = ["nmap", "whois", "whatweb", "wafw00f"]
        elif self.mode == "EXPLOIT":
            self.tool_sequence = ["sqlmap", "hydra", "weevely"]

    def compress_output(self, text):
        if not text: return "", False 
        text = str(text)
        success_keys = ["open", "200", "301", "critical", "high", "medium", "vulnerable", "found", "root", "admin", "service"]
        lines = [l.strip() for l in text.split('\n')]
        important = [l for l in lines if any(k in l.lower() for k in success_keys) or (len(l)<150 and "/" in l)]
        return "\n".join(important[:30]), (len(important) > 0)

    # --- FUNGSI PENTING: PEMBUAT PERINTAH AMAN ---
    def construct_safe_command(self, tool, target_input, log_file):
        tool = tool.lower().strip()
        
        # 1. Tentukan Format Target (Domain vs URL)
        if "://" in target_input:
            parsed = urlparse(target_input)
            domain_only = parsed.netloc if parsed.netloc else parsed.path
            full_url = target_input
        else:
            domain_only = target_input
            full_url = f"https://{target_input}"

        # 2. RUMUS PASTI UNTUK SETIAP ALAT (Hardcoded Syntax)
        # Ini mencegah AI salah ketik atau lupa flag penting
        
        cmd = ""
        
        if tool == "nmap":
            # Nmap butuh Domain/IP, bukan URL
            cmd = f"nmap -Pn -sT -T4 --top-ports 1000 {domain_only}"
            
        elif tool == "sqlmap":
            # WAJIB --batch agar tidak stuck minta input Y/N
            # WAJIB -u untuk URL
            cmd = f"sqlmap -u {full_url} --batch --random-agent --level=1 --timeout=10"
            
        elif tool == "arjun":
            # WAJIB -u
            cmd = f"arjun -u {full_url} -t 10 --timeout 5"
            
        elif tool == "nuclei":
            cmd = f"nuclei -u {full_url} -silent -timeout 5"
            
        elif tool == "wafw00f":
            cmd = f"wafw00f {domain_only}"
            
        elif tool == "feroxbuster":
            cmd = f"feroxbuster --url {full_url} --time-limit 5m --no-state"
            
        elif tool == "hydra":
            # Hydra butuh IP/Domain
            cmd = f"hydra -t 4 -l admin -P /usr/share/wordlists/rockyou.txt {domain_only} ssh -t 4"
            
        elif tool == "curl":
            cmd = f"curl -I {full_url} --max-time 10"
            
        elif tool == "whatweb":
            cmd = f"whatweb {full_url}"

        elif tool == "masscan":
             cmd = f"masscan {domain_only} -p1-1000 --rate=1000"
            
        else:
            # Default fallback
            cmd = f"{tool} {full_url}"

        # Tambahkan output ke log
        return f"{cmd} | tee {log_file}"

    def get_fallback_tool(self, current_step):
        # Rotasi alat jika AI bingung
        if current_step == 1: return "nmap"
        index = current_step % len(self.tool_sequence)
        return self.tool_sequence[index]

    def decide_next_action(self, target_input, log_dir, previous_output=None, current_step=1, tools_used_str=""):
        # Deteksi Scope di awal
        if current_step == 1:
            scope_type = self.auto_detect_scope(target_input)
            print(f"\033[1;35m[SYSTEM] Target Scope: {scope_type}\033[0m")

        # Persiapan data log
        raw_output = str(previous_output) if previous_output else ""
        clean_log, has_potential = self.compress_output(raw_output)
        
        last_tool = "unknown"
        if tools_used_str: last_tool = tools_used_str.split(",")[-1].strip()

        is_empty = len(raw_output) < 10
        report = f"[SYSTEM]: Tool '{last_tool}' finished. Findings: {has_potential}."

        # Prompt AI
        prompt = f"""
        [ROLE] Automated Pentest Operator.
        [TARGET] {target_input}
        [HISTORY] Step: {current_step} | Used: {tools_used_str}
        [LAST RESULT] {report}
        
        [TASK] Pick the NEXT tool from: {self.tool_sequence}
        [RULE] Output ONLY the tool name (e.g., 'nmap', 'nuclei'). nothing else.
        """
        
        user_msg = f"Last output summary:\n{clean_log}\n\nNext tool name?"
        if not previous_output: user_msg = "Start. Recommend first tool."

        # Minta nama alat ke AI
        response = self.engine.chat(prompt, user_msg)
        
        # Bersihkan respon AI (ambil kata pertama saja)
        tool_choice = response.strip().split()[0].lower() if response else ""
        
        # Validasi pilihan AI
        if tool_choice not in self.tool_sequence:
            # Jika AI ngawur atau diam, pakai rotasi otomatis
            tool_choice = self.get_fallback_tool(current_step)
            
        # Cegah pengulangan alat yang sama jika hasil sebelumnya kosong
        if tool_choice == last_tool and is_empty:
             tool_choice = self.get_fallback_tool(current_step + 1)

        # --- KONSTRUKSI PERINTAH YANG PASTI BENAR ---
        log_file = f"{log_dir}/{tool_choice}_step{current_step}.txt"
        final_cmd = self.construct_safe_command(tool_choice, target_input, log_file)
        
        return final_cmd