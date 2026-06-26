import chromadb
import uuid
import os

# Define o caminho para persistência do ChromaDB
CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")

def get_client():
    """
    Retorna o cliente persistente do ChromaDB.
    """
    return chromadb.PersistentClient(path=CHROMA_PATH)

def save_code_status(issue: str, status: str) -> None:
    """
    Salva o status de uma issue de código no ChromaDB.
    """
    client = get_client()
    # Pega ou cria a coleção para armazenar o status do código
    collection = client.get_or_create_collection(name="code_status_memory")
    
    # Cria um identificador único para este registro
    doc_id = str(uuid.uuid4())
    
    # O documento principal pode ser uma string descritiva que 
    # poderia ser usada em uma busca semântica no futuro
    document = f"Resumo da issue: {issue}. O status final do código foi: {status}."
    
    # Metadados são úteis para filtragem exata
    metadata = {
        "issue": issue,
        "status": status
    }
    
    # Adiciona na base vetorial (embedding será gerado automaticamente pelo ChromaDB caso não fornecido)
    collection.add(
        documents=[document],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"[ChromaStore] Status da issue salvo com sucesso no banco de dados. Doc ID: {doc_id}")
