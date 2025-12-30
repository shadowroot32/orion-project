from utils.ai_engine import AIEngine
import os

class AIAgent:
    def __init__(self, provider, api_key=None):
        self.engine = AIEngine(provider, api_key)

    def decide_next_action(self, target_url, previous_output=None, current_step=1, tools_used_str=""):
        
        # --- 1. FORCE PROGRESSION LOGIC (REM TANGAN) ---
        # Ini adalah logika Python murni untuk mencegah AI looping.
        # Jika WAFW00F sudah pernah dipakai, kita PAKSA dia pindah ke NUCLEI atau NMAP.
        
        used_list = tools_used_str.lower()
        
        # Skenario Macet di WAFW00F
        if "wafw00f" in used_list and current_step > 2:
            override_prompt = "DO NOT USE wafw00f. You already used it. MOVE TO NUCLEI or NMAP immediately."
        else:
            override_prompt = ""

        # --- 2. PROFILING & PROMPT ---
        target_type = "WEB"
        if target_url.startswith("*."): target_type = "WILDCARD"
        elif target_url.endswith(".apk"): target_type = "MOBILE_STATIC"
        
        system_prompt = f"""
        [ROLE]
        You are a Senior Red Team Operator.
        Target: {target_url} (Type: {target_type}) | Step: {current_step}
        
        [CRITICAL RULE: NO REPETITION]
        - Tools used so far: [{tools_used_str}]
        - **FORBIDDEN:** Do NOT use any tool listed in 'Tools used so far' again.
        - **MANDATORY:** You MUST switch to a new tool in every step if possible.
        - {override_prompt}

        [SYNTAX RULE]
        - ALWAYS USE `| tee logs/step{current_step}_tool.txt` (Never use `>`).
        - Output SINGLE LINE command.

        [ATTACK PROGRESSION]
        1. **IF wafw00f is done:** -> MOVE TO `nuclei -u {target_url} -t cves/ -o logs/nuclei.txt | tee logs/nuclei_disp.txt`
        2. **IF nuclei is done:** -> MOVE TO `feroxbuster -u {target_url} --depth 2 > logs/ferox.txt`
        3. **IF ferox is done:** -> MOVE TO `sqlmap -u "{target_url}" --batch --dbs | tee logs/sqlmap.txt`

        [DECISION]
        Based on previous output and used tools, what is the NEXT UNIQUE COMMAND?
        OUTPUT ONLY THE LINUX COMMAND.
        """

        if not previous_output:
            user_msg = f"Target: {target_url}. Step 1. Start Recon."
        else:
            safe_output = str(previous_output)[:4000]
            if len(safe_output) < 5:
                safe_output = "[WARNING: Output was empty. DO NOT REPEAT COMMAND. TRY SOMETHING ELSE.]"

            user_msg = f"""
            [PREVIOUS OUTPUT]:
            {safe_output}
            
            [INSTRUCTION]
            1. Tool '{tools_used_str}' has been used. PICK A DIFFERENT TOOL.
            2. If stuck, force run `nuclei` or `nmap`.
            
            Output ONLY the command.
            """

        response = self.engine.chat(system_prompt, user_msg)
        clean_cmd = response.replace("```bash", "").replace("```", "").replace("`", "").strip()
        clean_cmd = clean_cmd.replace("\n", " && ")

        # --- 3. SAFETY NET (Jaring Pengaman Terakhir) ---
        # Jika AI masih bandel ngasih 'wafw00f' lagi padahal sudah dipakai:
        if "wafw00f" in clean_cmd and "wafw00f" in used_list:
            # Kita bajak perintahnya, ganti paksa ke Nuclei/Nmap
            return f"nuclei -u {target_url} -t cves/ -o logs/step{current_step}_nuclei.txt | tee logs/step{current_step}_nuclei_display.txt"
            
        # Jika AI memberikan perintah kosong
        if not clean_cmd:
            return f"nmap -sV {target_url} | tee logs/step{current_step}_nmap.txt"

        return clean_cmd