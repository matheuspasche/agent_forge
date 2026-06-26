from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from nodes.refiner import run_refiner
from nodes.architect import run_architect
from nodes.developer import run_developer

def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("refiner", run_refiner)
    workflow.add_node("architect", run_architect)
    workflow.add_node("developer", run_developer)
    
    # Define edges
    workflow.add_edge(START, "refiner")
    workflow.add_edge("refiner", "architect")
    workflow.add_edge("architect", "developer")
    workflow.add_edge("developer", END)
    
    # Compile graph
    app = workflow.compile()
    
    return app

if __name__ == "__main__":
    app = create_graph()
    print("Graph compiled successfully")
