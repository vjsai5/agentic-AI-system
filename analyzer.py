
from utils.llm import LLMClient
class AnalyzerAgent:
    def __init__(self): self.llm=LLMClient()
    async def run(self,data):
        return self.llm.generate("Analyze and summarize:\n"+str(data))
