from app.graphs.simple_graph import SimpleGraph
from app.nodes.research_agent_parallel import research_agent_parallel

def dummy_node(state):
    # Simulate a node that processes the research results
    research_results = state.get("research_results", [])
    return {"summary": f"Summary of: {research_results}"}

graph = SimpleGraph()
graph.add_node("research", research_agent_parallel)
graph.add_node("summarize", dummy_node)
graph.add_edge("research", "summarize")

def run_expanded_graph(question):
    # Initial state
    state = {"question": question}
    # Run research node
    research_result = graph.run("research", state)
    # Add research results to state
    state["research_results"] = research_result["research_results"]
    # Run summarize node
    summary_result = graph.run("summarize", state)
    return summary_result

if __name__ == "__main__":
    result = run_expanded_graph("What is the latest in agentic AI research?")
    print(result)
