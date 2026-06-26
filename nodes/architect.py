from core.state import AgentState
import os

def run_architect(state: AgentState) -> dict:
    """
    Architect Node
    Implementa as skills '/to-prd' e '/to-issues' do padrão Matt Pocock.
    Converte a 'refined_idea' e 'CONTEXT.md' em um PRD formal e Issues fatiadas (Vertical Slices).
    """
    print("[Architect Node] Transformando ideias em PRD e Issues...")
    
    refined_idea = state.get("refined_idea", "")
    
    # Em uma implementação real com LangChain, chamaríamos o modelo 'architect' (Claude) aqui,
    # passando o `refined_idea` e solicitando a geração do PRD.
    
    prd_content = f"# PRD Gerado\n\nBaseado na ideia: {refined_idea}\n\n## Objetivos...\n(Simulado pelo Architect Node)"
    
    # Criar a pasta knowledge_base/ se não existir
    os.makedirs("knowledge_base/issues", exist_ok=True)
    
    prd_path = "knowledge_base/PRD_generated.md"
    with open(prd_path, "w", encoding="utf-8") as f:
        f.write(prd_content)
        
    print(f"[Architect Node] PRD salvo em {prd_path}")
    
    # Simulando a skill /to-issues
    issues = [
        "knowledge_base/issues/TASK-1.md",
        "knowledge_base/issues/TASK-2.md"
    ]
    
    for i, issue_path in enumerate(issues):
        with open(issue_path, "w", encoding="utf-8") as f:
            f.write(f"# Task {i+1}\n\nDetalhes da task (Simulado).")
            
    return {"prd_path": prd_path, "issues": issues, "current_issue": issues[0] if issues else None}
