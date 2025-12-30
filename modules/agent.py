from utils.ai_engine import AIEngine
import os

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)

    def decide_next_action(self, target_url, previous_output=None, current_step=1, tools_used_str=""):
        
        # --- 1. PROFILING TARGET ---
        target_type = "WEB"
        if target_url.startswith("*."): target_type = "WILDCARD"
        elif target_url.endswith(".apk"): target_type = "MOBILE_STATIC"
        
        # --- 2. OTAK RED TEAMER (THE BRAIN) ---
        system_prompt = f"""
        [ROLE]
        You are a Senior Red Team Operator (Human-like Logic) on Kali Linux.
        Target: {target_url} (Type: {target_type}) | Step: {current_step}

        [MINDSET: BE A PROFESSIONAL]
        1. **NO NOISE:** Don't run loud scans if a quiet one works.
        2. **MODERN TOOLS:** Prefer `nuclei` over `nikto`. Prefer `feroxbuster` over `dirb`.
        3. **CRITICAL FIRST:** Look for RCE, SQLi, and Env Leaks first.
        4. **LOGGING:** ALWAYS save to `logs/`. Ex: `-o logs/step{current_step}_tool.txt`.

        [ATTACK PLAYBOOKS]

        **STRATEGY A: WILDCARD RECON (*.domain)**
        - **Goal:** Expand attack surface.
        - `subfinder -d {str(target_url).replace('*.','')} -o logs/subfinder.txt`
        - `assetfinder -subs-only {str(target_url).replace('*.','')} | tee -a logs/assets.txt`
        - `httpx -l logs/assets.txt -status-code -title -o logs/live_hosts.txt` (Filter Live Hosts).

        **STRATEGY B: MOBILE STATIC (.apk)**
        - **Goal:** Secrets Extraction.
        - `strings {target_url} | grep -E "AKIA|AIza|Authorization|Bearer" > logs/tokens.txt`
        - `apktool d {target_url} -o logs/source_code`
        - *NOTE:* Manual review is usually required after this.

        **STRATEGY C: WEB APP "TOTAL WAR" (The Pro Flow)**
        
        *Phase 1: Fingerprinting & WAF Check*
        - `wafw00f {target_url} > logs/waf.txt`
        - `whatweb -a 3 {target_url} --log-verbose=logs/tech.txt`

        *Phase 2: Modern Vulnerability Scanning (The Nuclei Way)*
        - **GOLD STANDARD:** `nuclei -u {target_url} -t cves/ -t vulnerabilities/ -t exposures/ -o logs/nuclei_crit.txt`
        - *If Nuclei finds critical bugs, STOP and report.*

        *Phase 3: Fuzzing & Discovery*
        - `feroxbuster -u {target_url} -w common.txt --depth 2 --status-codes 200,301,403 > logs/ferox.txt`
        - `gobuster dir -u {target_url} -w common.txt -o logs/gobuster.txt`

        *Phase 4: Targeted Exploitation*
        - **SQLi:** `sqlmap -u "{target_url}" --batch --random-agent --level=2 --risk=2 > logs/sqlmap.txt`
        - **CMS (WP):** `wpscan --url {target_url} --enumerate p,t,u --plugins-detection aggressive > logs/wpscan.txt`
        - **Auth:** `hydra -l admin -P rockyou.txt {target_url} http-post-form ...`

        [DECISION LOGIC]
        - **Context:** Tools used: [{tools_used_str}].
        - **Analysis:** Look at previous output. 
          - Did WAF block us (403/406)? -> Use `--delay 2` or `-H "User-Agent: GoogleBot"`.
          - Did `nuclei` fail? -> Fallback to `nikto`.
          - Did we find `login.php`? -> Suggest `hydra`.
          - Did we find `.git`? -> Suggest `git-dumper`.
        
        OUTPUT ONLY THE LINUX COMMAND. NO EXPLANATION.
        """

        if not previous_output:
            if target_type == "WILDCARD":
                user_msg = "Step 1. Start Subdomain Enumeration (Subfinder/Assetfinder)."
            elif target_type == "MOBILE_STATIC":
                user_msg = f"Step 1. Extract Secrets from APK using strings."
            else:
                user_msg = f"Target: {target_url}. Step 1. Check for WAF and Tech Stack."
        else:
            safe_output = str(previous_output)[:6000]
            user_msg = f"""
            [PREVIOUS OUTPUT]:
            {safe_output}
            
            [INSTRUCTION]
            Act like a Lead Pentester. Analyze the output above.
            1. Is there a Critical CVE?
            2. Is there a WAF blocking us?
            3. What is the most logical next step to get a shell or data?
            
            Select the NEXT BEST COMMAND.
            """

        response = self.engine.chat(system_prompt, user_msg)
        clean_cmd = response.replace("```bash", "").replace("```", "").replace("`", "").strip()
        
        # Safety Fallback
        if not clean_cmd:
            return f"nuclei -u {target_url} -o logs/fallback_scan.txt"

        return clean_cmd