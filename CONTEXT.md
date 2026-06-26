# Domain Model: Agent Forge

## Core Terminology

- **Agent Forge**: O nome deste framework. É uma "fábrica de software autônoma" movida a IA.
- **Node (Nó)**: Uma etapa do fluxo no LangGraph. Cada nó representa um cargo ou fase do processo de engenharia de software (ex: Refiner, Architect, Developer).
- **Skill**: Uma habilidade encapsulada que resolve um problema específico. Podem ser de dois tipos:
  - **User-Invoked Skill**: Uma skill chamada pelo usuário humano (via CLI ou chat) para alinhar visão. Ex: `/grill-with-docs`.
  - **Model-Invoked Skill**: Uma skill que um agente (nó) chama de forma autônoma para resolver problemas técnicos. Ex: `/tdd`, `/diagnosing-bugs`.
- **DinD Manager**: O serviço que fala com o daemon do Docker para subir as sandboxes efêmeras.
- **Sandbox**: Um container temporário isolado criado apenas para rodar testes (Red-Green-Refactor).
- **Chroma Store / Vetorial Memory**: A memória de longo prazo onde logs passados e decisões são salvas para consulta futura (RAG).
- **Dogfooding**: O ato de usar o próprio Agent Forge para construir o Agent Forge.

## Architectural Conventions

- A CLI (`cli.py`) apenas invoca o LangGraph (`core.graph`). A lógica do negócio vive nos `nodes/`.
- Toda geração de código não testada é considerada insegura e deve ser direcionada para a **Sandbox** antes de ser aprovada pelo `Developer Node`.
- Arquivos gerados nas interações User-Invoked (PRD, Issues) devem sempre ser salvos fisicamente na pasta `knowledge_base/`.
