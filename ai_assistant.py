import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIVoiceAssistant:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "llama3-70b-8192"  # ✅ Updated model name

    def interact_with_llm(self, user_query):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_query}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("❌ Groq Error:", e)
            return f"Groq Error: {e}"
