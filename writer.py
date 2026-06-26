
from utils.llm import LLMClient
class WriterAgent:
    def __init__(self): self.llm=LLMClient()
    async def run(self,analysis):
        return self.llm.generate("Create professional report with recommendations:\n"+analysis)
