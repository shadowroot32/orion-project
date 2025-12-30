from utils.ai_engine import AIEngine

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)
        self.mode = "ALL"
        self.full_arsenal = [
            "wafw00f", "whatweb", "nuclei", "feroxbuster", "arjun", 
            "sqlmap", "hydra", "weevely", "msfvenom", "git-dumper", 
            "curl", "wget", "cloud_enum", "aws", "nmap", "ping", 
            "linpeas", "suid", "rm", "history"
        ]
        self.tool_sequence = self.full_arsenal

    def set_mode(self, mode_name):
        self.mode = mode_name.upper()
        if self.mode == "RECON": self.tool_sequence = ["wafw00f", "whatweb", "nmap", "whois"]
        elif self.mode == "DISCOVERY": self.tool_sequence = ["nuclei", "feroxbuster", "arjun"]
        elif self.mode == "EXPLOIT": self.tool_sequence = ["sqlmap", "hydra", "weevely", "linpeas"]
        elif self.mode == "CLOUD": self.tool_sequence = ["cloud_enum", "aws", "curl"]
        else: self.tool_sequence = self.full_arsenal

    def compress_output(self, text):
        if not text: return "", False 
        
        text = str(text)
        success_keys = ["open", "200", "301", "critical", "high", "medium", "vulnerable", "found", "root"]
        lines = [l.strip() for l in text.split('\n')]
        important = [l for l in lines if any(k in l.lower() for k in success_keys) or (len(l)<150 and "/" in l)]
        
        return "\n".join(important[:25]), (len(important) > 0)

    def get_fallback_tool(self, used_str):
        used = used_str.lower()
        for t in self.tool_sequence:
            if t not in used: return t
        return self.tool_sequence[0]

    def decide_next_action(self, target_url, log_dir, previous_output=None, current_step=1, tools_used_str=""):
        raw_output = str(previous_output) if previous_output else ""
        clean_log, has_potential = self.compress_output(raw_output)
        
        last_tool = "unknown"
        for t in self.full_arsenal:
            if t in tools_used_str.lower().split(",")[-1]: last_tool = t; break

        is_empty = len(raw_output) < 10
        report = f"[SYSTEM]: Tool '{last_tool}' failed/empty. SWITCH STRATEGY." if is_empty else "[SYSTEM]: Findings detected. Proceed."

        # PERBAIKAN PROMPT: Hapus instruksi path folder cves/ yang membingungkan AI
        prompt = f"""
        [ROLE] Elite Red Team Operator. Target: {target_url}
        [CONTEXT] Log Dir: {log_dir} | Allowed: {self.tool_sequence}
        [INSTRUCTION] MODE: {self.mode}. KILL CHAIN A-L.
        [STATUS] {report}
        [RULE] 
        1. ALWAYS use `| tee {log_dir}/filename.txt`. 
        2. Output SINGLE LINE command.
        3. For Nuclei, DO NOT use '-t' flag unless specific. Let it use default templates.
        """
        
        user_msg = f"Last Output:\n{clean_log}\n\nNext Step?"
        if not previous_output: user_msg = f"Target: {target_url}. Start Phase 1."

        cmd = self.engine.chat(prompt, user_msg).replace("```bash", "").replace("```", "").strip().replace("\n", " && ")
        
        # PERBAIKAN FALLBACK: Hapus '-t cves/' agar pakai template default sistem
        if not any(t in cmd for t in self.tool_sequence) and "cd" not in cmd:
            fb = self.get_fallback_tool(tools_used_str)
            if "nuclei" in fb: 
                # HAPUS "-t cves/" DISINI
                return f"nuclei -u {target_url} | tee {log_dir}/nuclei.txt"
            return f"{fb} {target_url} | tee {log_dir}/fallback.txt"
            
        return cmd