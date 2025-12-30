import os
import sys
from groq import Groq
from openai import OpenAI
import ollama

# --- SMART IMPORT GOOGLE ---
# Kode ini mencoba mendeteksi library mana yang Anda punya
GOOGLE_SDK_TYPE = None
try:
    # Coba Import Library Baru (V1.0 2024/2025)
    from google import genai
    GOOGLE_SDK_TYPE = "NEW"
except ImportError:
    try:
        # Jika gagal, Coba Import Library Lama
        import google.generativeai as genai_old
        GOOGLE_SDK_TYPE = "OLD"
    except ImportError:
        GOOGLE_SDK_TYPE = "NONE"

class AIEngine:
    def __init__(self, provider, api_key=None, model_name=None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.model_name = model_name
        
        # --- KONFIGURASI ENGINE ---
        if self.provider == "gemini":
            if not api_key: raise ValueError("Gemini API Key Required")
            
            if GOOGLE_SDK_TYPE == "NEW":
                # Setup SDK Baru
                self.client = genai.Client(api_key=api_key)
                self.model_name = model_name or "gemini-2.5-flash"
            elif GOOGLE_SDK_TYPE == "OLD":
                # Setup SDK Lama (Fallback)
                genai_old.configure(api_key=api_key)
                self.model_old = genai_old.GenerativeModel(model_name or "gemini-pro")
            else:
                raise ImportError("Library Google AI tidak terinstall! (pip install google-genai)")
            
        elif self.provider == "groq":
            if not api_key: raise ValueError("Groq API Key Required")
            self.client = Groq(api_key=api_key)
            self.model_name = model_name or "llama-3.3-70b-versatile" 
            
        elif self.provider == "openai":
            if not api_key: raise ValueError("OpenAI API Key Required")
            self.client = OpenAI(api_key=api_key)
            self.model_name = model_name or "gpt-4o"
            
        elif self.provider == "ollama":
            self.model_name = model_name or "llama3"
            try:
                ollama.list()
            except:
                print("Error: Ollama service mati.")

    def chat(self, system_prompt, user_message):
        """
        Fungsi chat universal.
        """
        try:
            # 1. GEMINI LOGIC
            if self.provider == "gemini":
                combined_prompt = f"{system_prompt}\n\n[USER INPUT]:\n{user_message}"
                
                if GOOGLE_SDK_TYPE == "NEW":
                    # Cara Baru
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=combined_prompt
                    )
                    return response.text.strip()
                elif GOOGLE_SDK_TYPE == "OLD":
                    # Cara Lama
                    response = self.model_old.generate_content(combined_prompt)
                    return response.text.strip()

            # 2. GROQ LOGIC
            elif self.provider == "groq":
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    model=self.model_name,
                    temperature=0.7,
                )
                return chat_completion.choices[0].message.content.strip()

            # 3. OPENAI LOGIC
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]
                )
                return response.choices[0].message.content.strip()

            # 4. OLLAMA LOGIC
            elif self.provider == "ollama":
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_message},
                ])
                return response['message']['content'].strip()

        except Exception as e:
            return f"AI Error ({self.provider}): {str(e)}"