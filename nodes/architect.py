from core.state import AgentState
import os
import subprocess
import re

def run_architect(state: AgentState, llm=None) -> dict:
    """
    Architect Node
    Converte a ideia em PRD e delega as Issues via GitHub.
    """
    print("[Architect Node] Transformando ideias em PRD e Issues no GitHub...")
    
    refined_idea = state.get("refined_idea", "Idea fallback")
    
    if llm:
        print(f"[Architect Node] Usando LLM instanciado: {llm.__class__.__name__}")
        
    prd_content = f"# PRD Gerado\n\nBaseado na ideia: {refined_idea}\n\n## Objetivos...\n(Simulado pelo Architect Node)"
    os.makedirs("knowledge_base/issues", exist_ok=True)
    
    prd_path = "knowledge_base/PRD_generated.md"
    with open(prd_path, "w", encoding="utf-8") as f:
        f.write(prd_content)
        
    print(f"[Architect Node] PRD salvo em {prd_path}")
    
    # Criar Issues Reais no GitHub (Skill /to-issues)
    issues_ids = []
    tasks = ["Implementar feature A baseada no PRD", "Adicionar testes unitários para a feature A"]
    
    for i, task_desc in enumerate(tasks):
        title = f"Task {i+1}: {task_desc[:20]}..."
        try:
            result = subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body", task_desc],
                capture_output=True, text=True, check=True
            )
            # Extrair a URL ou número da issue (ex: https://github.com/user/repo/issues/12)
            url = result.stdout.strip()
            match = re.search(r'/issues/(\d+)$', url)
            if match:
                issues_ids.append(match.group(1))
            print(f"[Architect Node] Issue criada no GitHub: {url}")
        except subprocess.CalledProcessError as e:
            print(f"[Architect Node] Falha ao criar issue: {e.stderr}")
            
    # Retorna os IDs das issues do GitHub (ex: ["12", "13"])
    return {"prd_path": prd_path, "issues": issues_ids, "current_issue": issues_ids[0] if issues_ids else None}
