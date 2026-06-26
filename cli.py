import argparse
import sys

def print_banner():
    banner = """
    ================================================
          🚀 Agent Forge - Agent Framework 🚀
    ================================================
    """
    print(banner)

from core.graph import create_graph

def start_project(idea: str):
    print(f"[!] Iniciando o Agent Forge com a ideia:")
    print(f"    -> \"{idea}\"")
    print("\n[+] Carregando configurações e conectando ao ChromaDB local...")
    
    print("\n[+] Compilando Grafo LangGraph...")
    app = create_graph()
    
    print("\n[+] Executando Agentes (Refiner -> Architect -> Developer)...")
    print("-" * 50)
    
    # Inicia o StateGraph com a ideia inicial
    final_state = app.invoke({"idea": idea})
    
    print("-" * 50)
    print("\n✅ Fluxo Finalizado!")
    print(f"-> PRD Gerado em: {final_state.get('prd_path')}")
    print(f"-> Última Issue Processada: {final_state.get('current_issue')}")
    print(f"-> Status do Código na Sandbox: {final_state.get('code_status')}")

def main():
    parser = argparse.ArgumentParser(description="Agent Forge CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando START
    start_parser = subparsers.add_parser("start", help="Inicia o refinamento de uma nova ideia")
    start_parser.add_argument("idea", type=str, help="A ideia bruta do projeto")

    # Comando SETUP
    setup_parser = subparsers.add_parser("setup", help="Inicia o wizard de chaves de API")

    args = parser.parse_args()

    print_banner()

    if args.command == "start":
        start_project(args.idea)
    elif args.command == "setup":
        import setup_keys
        setup_keys.setup_keys()

if __name__ == "__main__":
    main()
