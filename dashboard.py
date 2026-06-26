import streamlit as st
import subprocess
import json
import time

st.set_page_config(page_title="Agent Forge Telemetry", layout="wide", initial_sidebar_state="collapsed")

# CSS para Observabilidade (Tema Escuro, Estilo Datadog/Grafana)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
    }
    h1, h2, h3 { color: #58a6ff !important; }
    
    /* Terminal Console Style */
    .terminal-box {
        background-color: #010409;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 15px;
        font-family: 'Roboto Mono', monospace;
        color: #3fb950;
        height: 400px;
        overflow-y: scroll;
        white-space: pre-wrap;
    }
    
    /* Kanban Cards */
    .kanban-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .status-open { border-left: 4px solid #d29922; }
    .status-closed { border-left: 4px solid #238636; }
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Agent Forge Telemetry")
st.markdown("Monitoramento de Orquestradores, Subagentes (GitHub) e Sandboxes (Docker).")

# Fetch GitHub Issues
def fetch_issues():
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--state", "all", "--json", "number,title,state,updatedAt"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        return [{"title": "Erro ao conectar com GitHub CLI", "state": "ERROR", "number": 0}]

issues = fetch_issues()

col1, col2, col3 = st.columns([1, 2, 2])

with col1:
    st.subheader("🧠 Orquestrador")
    st.info("**StateGraph (LangGraph)**\n\nStatus: AGUARDANDO IDEIA VIA CLI\n\n- Nó Atual: `START`\n- Sandboxes Ativas: 0")
    if st.button("🔄 Force Refresh", help="Atualiza a tela"):
        st.rerun()

with col2:
    st.subheader("📦 Kanban (Subagentes)")
    
    col_todo, col_done = st.columns(2)
    
    with col_todo:
        st.markdown("**🏃 In Progress / To Do**")
        for iss in issues:
            if iss.get("state") == "OPEN":
                st.markdown(f"""
                <div class="kanban-card status-open">
                    <b>#{iss['number']}</b>: {iss['title']}
                </div>
                """, unsafe_allow_html=True)

    with col_done:
        st.markdown("**✅ Done**")
        for iss in issues:
            if iss.get("state") == "CLOSED":
                st.markdown(f"""
                <div class="kanban-card status-closed">
                    <b>#{iss['number']}</b>: {iss['title']}
                </div>
                """, unsafe_allow_html=True)

with col3:
    st.subheader("🐳 Docker DinD Logs")
    # Em produção real, este painel leria de um arquivo .log gravado pelo dind_manager.py
    st.markdown("""
    <div class="terminal-box">
> [DinD Manager] Serviço de Telemetria Iniciado. 
> Conectado ao socket docker.sock.
> Aguardando o Developer Node invocar a Sandbox...
> ...
> ...
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh simples a cada 5 segundos
time.sleep(5)
st.rerun()
