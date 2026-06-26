# ISSUE 4: Developer Node & Sandbox

## Contexto
O coração da execução. Ele lê a `current_issue`, gera código, e invoca o `dind_manager` para rodar na sandbox.

## Requisitos Técnicos
1. Em `sandbox/dind_manager.py`, criar classe que usa o `docker` (Python SDK) para iniciar um container efêmero (ex: `python:3.10-alpine`), copiar o código e rodar um script.
2. Em `nodes/developer.py`, usar o LLM para ler a issue, gerar código, escrever o arquivo e então invocar o `dind_manager`.
3. Atualizar o `state['code_status']` com 'SUCCESS' ou 'FAILED'.
