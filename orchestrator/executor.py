import asyncio
from agents.retriever import RetrieverAgent
from agents.analyzer import AnalyzerAgent
from agents.writer import WriterAgent
from orchestrator.batching import batch_tasks
from utils.logger import add_log

class Executor:
    def __init__(self,fail=False):
        self.r=RetrieverAgent(fail)
        self.a=AnalyzerAgent()
        self.w=WriterAgent()
    async def execute(self,plan,stream):
        tasks=[t for t in plan if t.task_type=='retrieval']
        results=[]
        for batch in batch_tasks(tasks,2):
            stream("Running retrieval batch")
            out=await asyncio.gather(*[self.r.run(t) for t in batch],return_exceptions=True)
            results.extend(out)
        stream("Analyzing")
        analysis=await self.a.run(results)
        stream("Writing report")
        report=await self.w.run(analysis)
        add_log("Workflow completed")
        return report
