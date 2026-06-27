
from tavily import TavilyClient
import os
class RetrieverAgent:
    def __init__(self, fail=False):
        self.fail=fail
        self.client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY",""))
    async def run(self, task):
        if self.fail: raise Exception("Simulated failure")
        r=self.client.search(query=task.description,max_results=5)
        return r.get("results",[])
