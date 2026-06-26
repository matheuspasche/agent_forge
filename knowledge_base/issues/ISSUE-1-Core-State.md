# ISSUE 1: Core Graph State & Initialization

## Contexto
O Agent Forge utiliza o LangGraph como orquestrador. Para isso, precisamos definir o `State` do grafo, que será a memória compartilhada entre todos os nós (agentes) durante uma execução.

## Requisitos Técnicos
1. No arquivo `core/state.py`, criar uma classe `AgentState` baseada em `TypedDict` do Python.
2. A classe deve conter:
   - `idea` (str): A ideia bruta do usuário.
   - `refined_idea` (str): A ideia após o grill-me.
   - `prd_path` (str): Caminho para o PRD gerado.
   - `issues` (list[str]): Caminhos para as issues geradas.
   - `current_issue` (str): A issue sendo trabalhada agora.
   - `code_status` (str): O status da compilação/teste na sandbox.
   - `messages` (Annotated[list, add_messages]): Histórico de conversa caso necessário.
3. No arquivo `core/graph.py`, criar a função de inicialização que vai ligar os nós, mas, por enquanto, faça apenas o setup básico para o grafo compilar.

## Como Validar
Um script simples que importa `AgentState` e consegue compilar um `StateGraph(AgentState)` sem erros sintáticos.
