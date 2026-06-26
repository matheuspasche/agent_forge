import os
import yaml
from core.state import AgentState

def run_refiner(state: AgentState) -> dict:
    """
    Refiner node that acts as an interviewer to get enough details about the idea.
    For this initial version, it enhances the idea with best practices without blocking for input.
    """
    idea = state.get("idea", "")
    
    # Read config/models.yaml to initialize the LLM
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, "config", "models.yaml")
    
    llm_model = "default-llm-model"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config and "llm" in config:
                llm_model = config["llm"].get("model", llm_model)
                
    system_prompt = (
        "You are an expert Software Architect. "
        "Your goal is to interview the user about their initial idea, "
        "asking clarifying questions to gather technical requirements, scale, and constraints "
        "before proceeding to the PRD generation."
    )
    
    print(f"[Refiner Node] Initializing LLM from config: {llm_model}")
    print(f"[Refiner Node] System Prompt loaded: {system_prompt}")
    print(f"[Refiner Node] Original Idea: {idea}")
    
    # Provisoriamente, apenas aprimora a ideia sozinho com melhores práticas
    refined_idea = (
        idea 
        + "\n\n--- Refined by Architect ---\n"
        + "Assumed Best Practices / Requirements:\n"
        + "- Containerized deployment (Docker)\n"
        + "- Standard Authentication & Authorization\n"
        + "- Robust error handling & logging"
    )
    
    print(f"[Refiner Node] Refined Idea:\n{refined_idea}\n")
    
    return {"refined_idea": refined_idea}
