from core.state import AgentState

def run_refiner(state: AgentState, llm=None) -> dict:
    """
    Refiner node that acts as an interviewer to get enough details about the idea.
    For this initial version, it enhances the idea with best practices without blocking for input.
    """
    idea = state.get("idea", "")
    
    system_prompt = (
        "You are an expert Software Architect. "
        "Your goal is to interview the user about their initial idea, "
        "asking clarifying questions to gather technical requirements, scale, and constraints "
        "before proceeding to the PRD generation."
    )
    
    if llm:
        print(f"[Refiner Node] Usando LLM instanciado: {llm.__class__.__name__}")
        # Aqui o llm poderia ser utilizado (e.g. llm.invoke)
    else:
        print("[Refiner Node] Nenhum LLM instanciado, usando simulação.")
        
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
