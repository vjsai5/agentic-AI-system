
from dataclasses import dataclass
@dataclass
class Task:
    id:int; task_type:str; description:str

class PlannerAgent:
    def create_plan(self, query):
        return [
            Task(1,"retrieval",f"Research: {query}"),
            Task(2,"retrieval",f"Latest trends about {query}"),
            Task(3,"analysis","Analyze findings"),
            Task(4,"writing","Generate report")
        ]
