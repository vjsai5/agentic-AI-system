
import os
from ollama import chat
MODEL=os.getenv("MODEL_NAME","gemma4")
class LLMClient:
    def generate(self,prompt):
        r=chat(model=MODEL,messages=[{"role":"user","content":prompt}])
        return r["message"]["content"]
