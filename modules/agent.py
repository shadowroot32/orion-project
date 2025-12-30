from utils.ai_engine import AIEngine

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)

    def decide_next_action(self, target_url, previous_output=None, current_step=1, tools_used_str=""):
        
        # --- THE ULTIMATE PROMPT ---
        # Menggabungkan Strategi Serangan Hacker dengan Kerapihan File Log
        
        system_prompt = f"""
        [ROLE]
        You are a Senior Red Team Operator & APT Simulator on Kali Linux.
        Target: {target_url} (Current Step: {current_step}).
        
        [RULE #1: MANDATORY LOGGING]
        **ALL OUTPUTS MUST BE SAVED TO 'logs/' DIRECTORY.**
        - Format: tool_name + step + .txt/.xml
        - Example: `nmap -oA logs/step{current_step}_nmap {target_url}`
        - Example: `nikto -h {target_url} -o logs/step{current_step}_nikto.txt`
        - Example: `sqlmap ... > logs/step{current_step}_sqlmap.txt`
        
        [RULE #2: ATTACK STRATEGY (TOTAL WAR MODE)]
        Do not stop at basic recon. Use this flow:
        
        1. **PHASE 1: RECON & DISCOVERY (Steps 1-15)**
           - `nmap -p- -sV` (Full Port Scan).
           - `whatweb -a 3` (Deep Tech Detect).
           - `wafw00f` (Firewall Detect).
           
        2. **PHASE 2: WEB ENUMERATION (Steps 16-40)**
           - `gobuster dir -u URL -w common.txt` (Find hidden folders).
           - `feroxbuster --depth 2` (Deep Fuzzing).
           - `nikto -Tuning x` (Server Misconfig).
           
        3. **PHASE 3: VULNERABILITY EXPLOITATION (Steps 41+)**
           - **IF SQL:** `sqlmap -u URL --batch --level=3 --risk=2`
           - **IF CMS (WP):** `wpscan --url URL --enumerate p,t,u --plugins-detection aggressive`
           - **IF JOOMLA:** `joomscan --url URL --ec`
           - **IF LOGIN FOUND:** `hydra -l user -P rockyou.txt ...`
           - **IF SSH/FTP:** `hydra` or `medusa`.
           
        4. **PHASE 4: EVASION & BYPASS (If blocked)**
           - Use `--random-agent`, `-f` (fragment), or `--delay 2`.

        [DECISION LOGIC]
        - Tools used so far: [{tools_used_str}]
        - **NEVER REPEAT** the exact same command.
        - If previous tool found nothing, TRY A DIFFERENT VECTOR (e.g., from Web -> Network -> API).
        - If step > 50 and stuck, try `arjun` (parameter discovery) or `commix`.
        
        OUTPUT ONLY THE LINUX COMMAND. NO EXPLANATION.
        """

        if not previous_output:
            user_msg = f"Target: {target_url}. Step 1. Start with Architecture Recon (Save output to logs/!)."
        else:
            # Membatasi output sebelumnya agar token tidak jebol
            safe_output = str(previous_output)[:6000]
            user_msg = f"""
            [PREVIOUS OUTPUT SUMMARY]:
            {safe_output}
            
            [TACTICAL ANALYSIS]
            1. Analyze the output above. What did we find? (Ports? CMS? Login? WAF?)
            2. Based on findings, select the NEXT BEST ATTACK from the Strategy List.
            3. **IMPORTANT:** Command MUST save output to 'logs/' folder.
            4. **IMPORTANT:** Do NOT use the same tool with same flags again. Vary the flags if you must use it again.
            
            Output ONLY the command.
            """

        response = self.engine.chat(system_prompt, user_msg)
        clean_cmd = response.replace("```bash", "").replace("```", "").replace("`", "").strip()
        
        # Safety Net: Jika AI nge-blank atau ngasih perintah kosong
        if not clean_cmd:
            return f"nmap -sV --script=vuln -oA logs/fallback_scan_{current_step} {target_url}"

        return clean_cmd