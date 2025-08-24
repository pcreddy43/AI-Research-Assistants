class SimpleGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, from_node, to_node):
        self.edges.setdefault(from_node, []).append(to_node)

    def run(self, start_node, state):
        current = start_node
        while current:
            func = self.nodes[current]
            result = func(state)
            # For demo, just run one node and stop
            return result

# Usage example:
from app.nodes.research_agent_parallel import research_agent_parallel

graph = SimpleGraph()
graph.add_node("research", research_agent_parallel)
# Add more nodes and edges as needed

# To run:
# state = {"question": "Your question here"}
# result = graph.run("research", state)
# print(result)
