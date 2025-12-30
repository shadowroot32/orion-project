from utils.ai_engine import AIEngine
import os
import re

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)

    def compress_output(self, text):
        """
        Fungsi ajaib untuk menghemat token.
        Hanya mengambil baris yang PENTING saja.
        """
        if not text: return ""
        
        lines = text.split('\n')
        important_lines = []
        
        # Kata kunci yang dicari (AI cuma butuh ini)
        keywords = ["open", "200", "301", "403", "critical", "high", "medium", "low", 
                    "vulnerable", "found", "detected", "title", "server", "admin", "login"]
        
        # Kata kunci sampah (Buang ini)
        junk_words = ["scanning", "time remaining", "eta", "percent", "progress", 
                      "starting", "finished", "yield", "warn", "info", "==="]

        for line in lines:
            line_lower = line.lower()
            
            # Jika baris mengandung sampah, lewati
            if any(junk in line_lower for junk in junk_words):
                continue
                
            # Jika baris mengandung info penting, ambil
            if any(key in line_lower for key in keywords):
                important_lines.append(line.strip())
            
            # Ambil baris pendek yang mungkin berisi nama file
            elif len(line) < 100 and "/" in line:
                important_lines.append(line.strip())

        # Gabungkan kembali, batasi max 1500 karakter (Hemat Token!)
        result = "\n".join(important_lines)
        return result[:1500]

    def decide_next_action(self, target_url, previous_output=None, current_step=1, tools_used_str=""):
        
        # --- 1. FORCE PROGRESSION (ANTI-LOOP) ---
        used_list = tools_used_str.lower()
        override_prompt = ""
        
        if "wafw00f" in used_list and current_step > 2:
            override_prompt = "RECON DONE. MOVE TO DISCOVERY (Nuclei/Arjun)."
        if "nuclei" in used_list and current_step > 10:
            override_prompt = "DISCOVERY DONE. MOVE TO EXPLOIT OR PRIVESC."

        # --- 2. PROFILING ---
        target_type = "WEB"
        if target_url.startswith("*."): target_type = "WILDCARD"
        elif target_url.endswith(".apk"): target_type = "MOBILE_STATIC"
        
        domain_keyword = target_url.replace("https://", "").replace("http://", "").split('.')[0]

        system_prompt = f"""
        [ROLE]
        Elite Red Team Operator. Target: {target_url} | Step: {current_step}
        
        [RULE]
        1. **USE `| tee`** always.
        2. **NO REPETITION.** {override_prompt}
        3. **BE EFFICIENT.** Do not run same scan twice.

        [STRATEGY: KILL CHAIN A-L]
        A: Recon (wafw00f, whatweb)
        B: Discovery (nuclei, feroxbuster)
        G: Guerrilla (arjun params)
        C: Exploit (sqlmap, hydra)
        E: Weapon (weevely backdoor)
        F: Loot (git-dumper, env)
        H: Cloud (cloud_enum, aws s3)
        I: Internal (nmap local)
        K: PrivEsc (linpeas)
        L: CleanUp (rm logs)

        [DECISION]
        - Check output below.
        - If 'Found' -> Exploit/Loot.
        - If 'Nothing' -> Next Strategy.
        - Stuck? -> Run 'nuclei' or 'arjun'.
        
        OUTPUT ONLY THE LINUX COMMAND (SINGLE LINE).
        """

        if not previous_output:
            user_msg = f"Target: {target_url}. Step 1. Start Recon."
        else:
            # --- 3. FILTERING (RAHASIA HEMAT TOKEN) ---
            # Kita bersihkan output sebelum dikirim ke AI
            raw_output = str(previous_output)
            clean_output = self.compress_output(raw_output)
            
            # Jika output kosong setelah dibersihkan, beri peringatan hemat
            if len(clean_output) < 5:
                clean_output = "[Log Cleaned: No critical findings in last step. Proceed to next tool.]"

            user_msg = f"""
            [SUMMARY OF FINDINGS]:
            {clean_output}
            
            [INSTRUCTION]
            Based on findings above, what is the NEXT BEST STEP?
            Output ONLY the command.
            """

        response = self.engine.chat(system_prompt, user_msg)
        clean_cmd = response.replace("```bash", "").replace("```", "").replace("`", "").strip()
        clean_cmd = clean_cmd.replace("\n", " && ")

        # Safety Override
        if "wafw00f" in clean_cmd and "wafw00f" in used_list:
            return f"nuclei -u {target_url} -t cves/ | tee logs/step{current_step}_nuclei.txt"
            
        if not clean_cmd:
            return f"nmap -sV {target_url} | tee logs/fallback.txt"

        return clean_cmd