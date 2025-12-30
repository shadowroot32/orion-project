from utils.ai_engine import AIEngine

class AIAgent:
    def __init__(self, provider, api_key=None):
        # Inisialisasi Engine yang dipilih user
        self.engine = AIEngine(provider, api_key)

    def decide_next_action(self, target_url, previous_output=None, current_step=1, tools_used_str=""):
        
        system_prompt = f"""
        [ROLE]
        You are an Elite Red Team Automation Engine on Kali Linux.
        Goal: Use EVERY RELEVANT TOOL available in Kali Linux to audit: {target_url}.
        Current Step: {current_step}. Used Tools: [{tools_used_str}].
        
        [ARSENAL - USE VARIETY!]
        1. Recon: nmap, masscan, whatweb, wafw00f, sublist3r, dnsenum.
        2. Web Enum: gobuster, dirb, feroxbuster, nikto.
        3. CMS: wpscan, joomscan, droopescan.
        4. Vuln: searchsploit, sqlmap, xsser, commix.
        5. Pass: hydra, medusa.
        
        [RULES]
        1. OUTPUT ONLY THE LINUX COMMAND. NO MARKDOWN.
        2. BE AGGRESSIVE. If port 80 open, scan dirs. If login found, brute force.
        3. CLI ONLY: Use non-interactive flags (-batch, --no-interactive).
        4. Do NOT repeat the exact same command.
        """

        if not previous_output:
            user_msg = f"Target: {target_url}. Step 1. Start Reconnaissance."
        else:
            safe_output = str(previous_output)[:6000]
            user_msg = f"""
            [PREVIOUS OUTPUT]:
            {safe_output}
            
            [INSTRUCTION]
            Analyze output. Pick the NEXT BEST TOOL from Kali Linux arsenal.
            Output ONLY the command.
            """

        # Panggil Engine Universal
        response = self.engine.chat(system_prompt, user_msg)
        
        # Bersihkan format
        clean_cmd = response.replace("```bash", "").replace("```", "").replace("`", "").strip()
        return clean_cmd