import os

def setup_keys():
    print("=============================================")
    print("   Agent Forge - Setup de Chaves de API   ")
    print("=============================================\n")
    
    print("Para que os Agentes funcionem, precisamos configurar as chaves das LLMs.")
    print("Você pode pular as que não possuir apertando Enter.\n")
    
    keys = {}
    
    # Gemini
    print("1. Google Gemini (Recomendado para Codificação/Testes rápidos e baratos)")
    print("   Obtenha em: https://aistudio.google.com/app/apikey")
    keys['GOOGLE_API_KEY'] = input("   Sua GOOGLE_API_KEY: ").strip()
    
    # Claude
    print("\n2. Anthropic Claude (Recomendado para Arquitetura e Refinamento de alto nível)")
    print("   Obtenha em: https://console.anthropic.com/settings/keys")
    keys['ANTHROPIC_API_KEY'] = input("   Sua ANTHROPIC_API_KEY: ").strip()
    
    # OpenAI
    print("\n3. OpenAI (Opção flexível, GPT-4o)")
    print("   Obtenha em: https://platform.openai.com/api-keys")
    keys['OPENAI_API_KEY'] = input("   Sua OPENAI_API_KEY: ").strip()
    
    with open(".env", "w") as f:
        for k, v in keys.items():
            if v:
                f.write(f"{k}={v}\n")
            else:
                f.write(f"#{k}=\n")
                
    print("\n✅ Arquivo .env gerado com sucesso!")
    print("Lembre-se: O arquivo .env NUNCA deve ser commitado. Já vamos garantir isso no .gitignore.")

if __name__ == "__main__":
    setup_keys()
