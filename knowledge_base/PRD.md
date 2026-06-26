# Product Requirements Document (PRD): Agent Forge

## 1. Visão Geral
**Agent Forge** é um framework para desenvolvimento autônomo baseado em IA. Ele converte ideias brutas em software executável, testado e documentado através de uma rede orquestrada de agentes com habilidades específicas, operando em sandboxes seguras (Docker-in-Docker) e mantendo memória contínua de todo o ciclo de vida do projeto.

## 2. Objetivos Principais
- **Refinamento de Ideia:** Permitir a evolução de uma ideia vaga para um PRD concreto através de "grilling" com a IA.
- **Desenvolvimento Autônomo Seguro:** Evitar que agentes LLM quebrem o ambiente local ou entrem em loops infinitos. Para isso, o desenvolvimento e os testes rodam em sandboxes Docker isoladas e efêmeras.
- **Roteamento Dinâmico de LLMs:** Permitir a utilização do melhor LLM para cada tarefa (ex: Claude para arquitetura, Gemini para código, OpenAI para revisão).
- **Memória de Longo Prazo:** Indexação de tudo o que foi planejado, codificado e discutido em um banco de dados vetorial local (ChromaDB).

## 3. Público-Alvo
- Desenvolvedores individuais que desejam multiplicar sua produtividade.
- Arquitetos de software que precisam prototipar ideias rapidamente com alta qualidade.

## 4. Escopo do Produto (MVP)
### 4.1 Interface e UX
- CLI em Python que aceita comandos como `agent_forge start "Criar uma API de to-do"`.
- Acompanhamento visual da execução no LangGraph Studio.

### 4.2 Fluxo Principal (LangGraph Nodes)
1. **Refinement Node (Entrevistador):** Pergunta até não haver ambiguidades. Requer aprovação humana (human-in-the-loop).
2. **Productization Node (Arquiteto):** Gera PRD, Issues e define a arquitetura no `knowledge_base/`.
3. **Development Node (Coder + Tester):** Lê as issues, gera código, e inicia ciclos Ralph TDD em um container Docker efêmero.
4. **Documentation Node (Reporter):** Registra o que foi feito, o tempo gasto, e atualiza o histórico do projeto.

### 4.3 Segurança e Limitações
- Timeout rígido para agentes (evitar custo alto).
- Execução de comandos estritamente isolada no DinD.

## 5. Casos de Uso
1. O usuário tem uma ideia ("quero um script de automação no N8N").
2. Roda a CLI `agent_forge start`.
3. O agente entrevistador faz 3 perguntas sobre integrações e fluxos.
4. O usuário responde. O agente arquiteto aprova e cria o plano.
5. O agente de desenvolvimento escreve os containers, scripts e roda testes na sandbox.
6. O sistema devolve o projeto pronto com documentação de como rodar.
