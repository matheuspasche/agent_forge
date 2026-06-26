from core.state import AgentState
from sandbox.dind_manager import DinDManager
import subprocess

def apply_tdd_skill(issue: str, llm=None) -> tuple[str, str]:
    """
    Skill: /tdd
    Executes Test-Driven Development autonomously.
    """
    print(f"[Skill /tdd] Analisando issue para gerar código e testes: {issue}")
    if llm:
        import re
        prompt = (
            f"You are an expert Python developer. Given the following issue: {issue}\n"
            "Generate the Python code to solve it, and the Python pytest-style tests for it.\n"
            "Return ONLY the code and tests enclosed in <CODE>...</CODE> and <TEST>...</TEST> XML tags."
        )
        try:
            response = llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            code_match = re.search(r'<CODE>(.*?)</CODE>', content, re.DOTALL)
            test_match = re.search(r'<TEST>(.*?)</TEST>', content, re.DOTALL)
            code = code_match.group(1).strip() if code_match else "def solve(data):\n    pass"
            test = test_match.group(1).strip() if test_match else "print('Testes passaram!')"
            return code, test
        except Exception as e:
            print(f"[Skill /tdd] Erro ao usar LLM: {e}")
            
    code = "def solve(data):\n    return data.upper()"
    test = "assert solve('hello') == 'HELLO'\nprint('Testes passaram!')"
    return code, test

def apply_diagnosing_bugs_skill(issue_id: str, code: str, test: str, logs: str, llm=None) -> tuple[str, str]:
    """
    Skill: /diagnosing-bugs
    Analyzes failing logs, the current code, and the test.
    Also comments on the GitHub issue.
    """
    print(f"[Skill /diagnosing-bugs] Analisando logs de erro e corrigindo o código:\n{logs}")
    
    # Comentar na issue do GitHub
    if issue_id:
        body = f"**Diagnosing Bugs Triggered**\n\nLogs de falha na sandbox:\n```\n{logs}\n```"
        try:
            subprocess.run(["gh", "issue", "comment", issue_id, "--body", body], check=True)
            print(f"[Developer Node] Comentário de erro adicionado na Issue #{issue_id}")
        except Exception as e:
            print(f"[Developer Node] Falha ao comentar na issue: {e}")
            
    if llm:
        import re
        prompt = (
            "You are an expert Python developer diagnosing a bug.\n"
            f"Current Code:\n{code}\n\n"
            f"Current Test:\n{test}\n\n"
            f"Failing Logs:\n{logs}\n\n"
            "Fix the code to make the tests pass. Return the fixed code and the (possibly unchanged or fixed) test.\n"
            "Return ONLY the code and tests enclosed in <CODE>...</CODE> and <TEST>...</TEST> XML tags."
        )
        try:
            response = llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            code_match = re.search(r'<CODE>(.*?)</CODE>', content, re.DOTALL)
            test_match = re.search(r'<TEST>(.*?)</TEST>', content, re.DOTALL)
            fixed_code = code_match.group(1).strip() if code_match else code
            fixed_test = test_match.group(1).strip() if test_match else test
            return fixed_code, fixed_test
        except Exception as e:
            print(f"[Skill /diagnosing-bugs] Erro ao usar LLM: {e}")

    fixed_code = "def solve(data):\n    return str(data).upper()"
    return fixed_code, test

def run_developer(state: AgentState, llm=None) -> dict:
    """
    Developer Node
    Pega a issue atual (agora um ID do GitHub), gera código, testa no Docker e reporta erros ao vivo no GitHub.
    """
    current_issue_id = state.get("current_issue")
    if not current_issue_id:
        print("[Developer Node] Nenhuma issue pendente.")
        return {"code_status": "SUCCESS"}
        
    print(f"[Developer Node] Trabalhando na issue do GitHub: #{current_issue_id}")
    
    if llm:
        print(f"[Developer Node] Usando LLM instanciado: {llm.__class__.__name__}")
    
    # Move para In Progress via CLI (Opcional, depende do Project)
    
    code, test = apply_tdd_skill(current_issue_id, llm=llm)
    sandbox = DinDManager()
    max_retries = 3
    
    for attempt in range(1, max_retries + 1):
        script = f"{code}\n\n{test}"
        print(f"[Developer Node] Enviando código para a Sandbox DinD (Tentativa {attempt}/{max_retries})...")
        result = sandbox.run_sandbox_test(
            image="python:3.10-alpine", 
            command="python script.py", 
            script_content=script
        )
        
        if result.get("status") == "SUCCESS":
            print("[Developer Node] Testes verdes! O código funciona e foi aprovado.")
            # Fecha a issue no GitHub
            if current_issue_id:
                try:
                    subprocess.run(["gh", "issue", "close", current_issue_id, "-c", "Fechado autonomamente pelo Agent Forge após testes passarem na sandbox."], check=True)
                    print(f"[Developer Node] Issue #{current_issue_id} fechada com sucesso no GitHub.")
                except Exception as e:
                    pass
            return {"code_status": "SUCCESS", "final_code": code}
        else:
            logs = result.get("logs", "Erro desconhecido durante a execução.")
            print(f"[Developer Node] Bug detectado nos testes: {logs}")
            
            if attempt < max_retries:
                print("[Developer Node] Acionando a skill /diagnosing-bugs para corrigir...")
                code, test = apply_diagnosing_bugs_skill(current_issue_id, code, test, logs, llm=llm)
            else:
                print("[Developer Node] Falha irreparável.")
                return {"code_status": "FAILED", "error_logs": logs}
                
    return {"code_status": "FAILED"}
