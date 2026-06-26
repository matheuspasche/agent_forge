from core.state import AgentState
from memory.chroma_store import save_code_status

def run_reporter(state: AgentState) -> dict:
    """
    Reporter Node
    Lê o status da issue que acabou de ser fechada pelo workflow 
    e o persiste no banco vetorial ChromaDB, utilizando a memória de longo prazo.
    """
    print("[Reporter Node] Iniciando o registro na memória (ChromaDB)...")
    
    current_issue = state.get("current_issue")
    code_status = state.get("code_status")
    
    if current_issue and code_status:
        print(f"[Reporter Node] Registrando status '{code_status}' para a issue: '{current_issue}'")
        try:
            save_code_status(issue=current_issue, status=code_status)
            print("[Reporter Node] Memória atualizada com sucesso.")
        except Exception as e:
            print(f"[Reporter Node] Erro ao salvar no banco vetorial: {e}")
    else:
        print("[Reporter Node] Informações insuficientes no state para salvar na memória. Faltando issue ou code_status.")
        
    return {}
