from core.state import AgentState
from sandbox.dind_manager import DinDManager

def run_developer(state: AgentState) -> dict:
    """
    Developer Node
    Implementa as skills Model-Invoked: '/tdd', '/diagnosing-bugs' e '/codebase-design'.
    Pega a issue atual, gera código (e testes), envia para o DinD, avalia os erros e refatora (Ralph Loop).
    """
    print("[Developer Node] Iniciando ciclo TDD (Red-Green-Refactor) para a Issue...")
    
    current_issue = state.get("current_issue")
    if not current_issue:
        print("[Developer Node] Nenhuma issue pendente.")
        return {"code_status": "SUCCESS"}
        
    print(f"[Developer Node] Trabalhando na issue: {current_issue}")
    
    # Simulação da geração de código por um LLM (Gemini)
    mock_code = "def add(a, b): return a + b"
    mock_test = "assert add(2,2) == 4"
    script = f"{mock_code}\n{mock_test}\nprint('Testes passaram!')"
    
    # Invoca o Sandbox para testar
    sandbox = DinDManager()
    
    # Roda no ambiente isolado (exemplo com python-alpine)
    print("[Developer Node] Enviando código para a Sandbox DinD...")
    result = sandbox.run_sandbox_test(
        image="python:3.10-alpine", 
        command="python script.py", 
        script_content=script
    )
    
    # Avaliação do resultado pelo Revisor LLM (Simulado)
    if result["status"] == "SUCCESS":
        print("[Developer Node] Testes verdes! O código funciona.")
        return {"code_status": "SUCCESS"}
    else:
        print(f"[Developer Node] Bug detectado: {result['logs']}")
        print("[Developer Node] Iniciando loop de /diagnosing-bugs...")
        return {"code_status": "FAILED"}
