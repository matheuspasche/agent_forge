from core.state import AgentState
from sandbox.dind_manager import DinDManager

def apply_tdd_skill(issue: str) -> tuple[str, str]:
    """
    Skill: /tdd
    Executes Test-Driven Development autonomously.
    Takes an issue description, generates a failing test (Red), and then the code to pass it (Green).
    """
    print(f"[Skill /tdd] Analisando issue para gerar código e testes: {issue}")
    # Simulação da geração de código por um LLM
    code = "def solve(data):\n    return data.upper()"
    test = "assert solve('hello') == 'HELLO'\nprint('Testes passaram!')"
    return code, test

def apply_diagnosing_bugs_skill(code: str, test: str, logs: str) -> tuple[str, str]:
    """
    Skill: /diagnosing-bugs
    Analyzes failing logs, the current code, and the test.
    Returns the fixed code and test.
    """
    print(f"[Skill /diagnosing-bugs] Analisando logs de erro e corrigindo o código:\n{logs}")
    # Simulação da correção de bug por um LLM
    fixed_code = "def solve(data):\n    return str(data).upper()"
    return fixed_code, test

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
    
    # 1. Aplica a skill /tdd para gerar a base de código e testes
    code, test = apply_tdd_skill(current_issue)
    
    sandbox = DinDManager()
    max_retries = 3
    
    # Loop de Refatoração / Correção de Bugs
    for attempt in range(1, max_retries + 1):
        script = f"{code}\n\n{test}"
        
        print(f"[Developer Node] Enviando código para a Sandbox DinD (Tentativa {attempt}/{max_retries})...")
        result = sandbox.run_sandbox_test(
            image="python:3.10-alpine", 
            command="python script.py", 
            script_content=script
        )
        
        # Avaliação do resultado
        if result.get("status") == "SUCCESS":
            print("[Developer Node] Testes verdes! O código funciona e foi aprovado.")
            return {"code_status": "SUCCESS", "final_code": code}
        else:
            logs = result.get("logs", "Erro desconhecido durante a execução.")
            print(f"[Developer Node] Bug detectado nos testes: {logs}")
            
            if attempt < max_retries:
                print("[Developer Node] Acionando a skill /diagnosing-bugs para corrigir...")
                code, test = apply_diagnosing_bugs_skill(code, test, logs)
            else:
                print("[Developer Node] Falha: Não foi possível corrigir o bug após múltiplas tentativas.")
                return {"code_status": "FAILED", "error_logs": logs}
                
    return {"code_status": "FAILED"}
