# ISSUE 3: Architect Node (Productization)

## Contexto
O Architect Node é responsável por pegar a `refined_idea` (saída do Refiner Node) e transformá-la em um PRD e uma lista de Issues (exatamente como estamos fazendo agora), salvando tudo em Markdown na pasta `knowledge_base/`.

## Requisitos Técnicos
1. Em `nodes/architect.py`, criar `run_architect(state: AgentState)`.
2. Usar o LLM para gerar um documento Markdown com o título "PRD e Plano de Ação".
3. Salvar o documento fisicamente em `knowledge_base/PRD_generated.md`.
4. Atualizar o `state['prd_path']` com o caminho do arquivo gerado.
