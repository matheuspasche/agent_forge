# ISSUE 2: Refiner Node (Grill-me)

## Contexto
O nó Refiner é o primeiro passo da execução do Agent Forge. Ele atua como um entrevistador. Ele recebe a `idea` original e deve questionar o usuário até ter detalhes suficientes.

## Requisitos Técnicos
1. No arquivo `nodes/refiner.py`, crie a função `run_refiner(state: AgentState) -> dict`.
2. A função deve ler a configuração em `config/models.yaml` para saber qual LLM inicializar.
3. Crie um prompt de sistema onde o Agente age como um arquiteto perguntando detalhes sobre a ideia.
4. (Simulação de Human-in-the-loop): Para esta primeira versão, podemos simular que o LLM gera as perguntas e aguardamos o input via terminal (ou, provisoriamente, o LLM apenas aprimora a ideia sozinho com base nas melhores práticas para não bloquear o fluxo em loop infinito durante o desenvolvimento inicial).

## Como Validar
Deve ser possível injetar esse nó no grafo principal em `core/graph.py` e ver o console imprimir as perguntas ou a ideia refinada.
