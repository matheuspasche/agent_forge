import os
import yaml
from functools import partial
from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from nodes.refiner import run_refiner
from nodes.architect import run_architect
from nodes.developer import run_developer

def get_llm_for_node(node_name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, "config", "models.yaml")
    
    if not os.path.exists(config_path):
        return None
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    agents_config = config.get("agents", {})
    node_config = agents_config.get(node_name)
    
    if not node_config:
        return None
        
    provider = node_config.get("provider")
    model = node_config.get("model")
    temperature = node_config.get("temperature", 0.0)
    
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model_name=model, temperature=temperature)
    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model, temperature=temperature)
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=model, temperature=temperature)
    
    return None

def create_graph():
    workflow = StateGraph(AgentState)
    
    refiner_llm = get_llm_for_node("refiner")
    architect_llm = get_llm_for_node("architect")
    
    # Add nodes
    workflow.add_node("refiner", partial(run_refiner, llm=refiner_llm))
    workflow.add_node("architect", partial(run_architect, llm=architect_llm))
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
