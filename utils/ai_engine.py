import google.generativeai as genai
from groq import Groq
from openai import OpenAI
import requests

class AIEngine:
    def __init__(self, provider, api_key=None):
        self.provider = provider
        self.api_key = api_key
        try:
            if provider == "gemini":
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            elif provider == "groq":
                self.client = Groq(api_key=api_key)
            elif provider == "openai":
                self.client = OpenAI(api_key=api_key)
        except Exception as e:
            print(f"[!] AI Init Error: {e}")

    def chat(self, system_prompt, user_message):
        try:
            if self.provider == "gemini":
                chat = self.model.start_chat(history=[])
                return chat.send_message(f"{system_prompt}\n\nUser Input: {user_message}").text
            elif self.provider == "groq":
                completion = self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                    temperature=0.6
                )
                return completion.choices[0].message.content
            elif self.provider == "openai":
                completion = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                    temperature=0.6
                )
                return completion.choices[0].message.content
            elif self.provider == "ollama":
                url = "http://localhost:11434/api/generate"
                payload = {"model": "mistral", "prompt": f"{system_prompt}\n\n{user_message}", "stream": False}
                return requests.post(url, json=payload).json().get("response", "")
        except Exception as e:
            return f"Error from AI: {str(e)}"