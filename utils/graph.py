from graphviz import Digraph
def build_graph():
    g=Digraph()
    g.edge('Planner','Retriever')
    g.edge('Retriever','Analyzer')
    g.edge('Analyzer','Writer')
    return g
