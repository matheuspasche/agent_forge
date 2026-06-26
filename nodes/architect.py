from core.state import AgentState
import os
import subprocess
import re
import json
from langchain_core.messages import SystemMessage, HumanMessage

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
    tasks = []
    
    if llm:
        system_msg = SystemMessage(content="You are a technical architect. Break down the following project idea into a list of specific, actionable tasks. Return ONLY a valid JSON array of strings, where each string is a task description.")
        human_msg = HumanMessage(content=f"Idea: {refined_idea}")
        
        try:
            response = llm.invoke([system_msg, human_msg])
            content = response.content
            
            # Tenta extrair o array JSON caso haja markdown ao redor
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                tasks = json.loads(json_match.group(0))
            else:
                tasks = json.loads(content)
        except Exception as e:
            print(f"[Architect Node] Erro ao usar LLM para gerar tasks: {e}")
            tasks = ["Implementar feature baseada no PRD (Fallback)"]
    else:
        tasks = ["Implementar feature baseada no PRD (Fallback sem LLM)"]
    
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
