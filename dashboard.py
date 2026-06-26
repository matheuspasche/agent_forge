import streamlit as st
import subprocess
import json
import time

st.set_page_config(page_title="Agent Forge Telemetry", layout="wide", initial_sidebar_state="collapsed")

# CSS Premium (Glassmorphism, Gradients, Hover Effects)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Reset & Background */
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif !important;
        background: radial-gradient(circle at 10% 20%, #0b0f19 0%, #111827 100%) !important;
        color: #f8fafc !important;
    }
    
    /* Esconde barra superior do Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Título com Gradiente */
    h1 {
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }

    /* Glassmorphism Panels */
    .glass-panel {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
    }
    
    .glass-panel h3 {
        font-weight: 600;
        color: #e2e8f0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 12px;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }

    /* Kanban Cards Premium */
    .kanban-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .kanban-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Badges de Status Lateral */
    .status-open::before {
        content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
        background: #f59e0b; /* Amber */
    }
    .status-closed::before {
        content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
        background: #10b981; /* Emerald */
    }

    .issue-id { color: #8b5cf6; font-weight: 800; font-size: 0.9rem; margin-bottom: 6px; display: inline-block; }
    .issue-title { color: #f1f5f9; font-weight: 400; font-size: 1.05rem; line-height: 1.4; }

    /* Vercel-like Terminal */
    .terminal-container {
        background: #000000;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        overflow: hidden;
    }
    .terminal-header {
        background: #111;
        padding: 10px 15px;
        border-bottom: 1px solid #333;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .mac-btn { width: 12px; height: 12px; border-radius: 50%; }
    .close { background: #ff5f56; } .min { background: #ffbd2e; } .max { background: #27c93f; }
    .terminal-body {
        padding: 20px;
        font-family: 'JetBrains Mono', monospace;
        color: #10b981;
        height: 500px;
        overflow-y: scroll;
        white-space: pre-wrap;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Esconder headers padrão do st.subheader pra usar os do CSS */
    .st-emotion-cache-10trblm { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Agent Forge Telemetry</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Live Monitoring: Orchestrators, Agents & Dockers</p>", unsafe_allow_html=True)

# Fetch GitHub Issues (Real Data)
def fetch_issues():
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--state", "all", "--json", "number,title,state,updatedAt"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        return [{"title": "Connection failed. Is 'gh' authenticated?", "state": "ERROR", "number": 0}]

issues = fetch_issues()

col1, col2, col3 = st.columns([1, 1.2, 1.8], gap="large")

with col1:
    st.markdown("""
    <div class="glass-panel">
        <h3>🧠 Orchestrator State</h3>
        <div style="padding: 10px 0;">
            <p style="color:#94a3b8; font-size:0.9rem; margin-bottom:5px;">ACTIVE WORKFLOW</p>
            <p style="font-size:1.2rem; font-weight:600; color:#38bdf8;">LangGraph: Waiting for CLI</p>
        </div>
        <div style="padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.05);">
            <p style="color:#94a3b8; font-size:0.9rem; margin-bottom:5px;">CURRENT NODE</p>
            <p style="font-size:1.2rem; font-weight:600; color:#f472b6;">● START</p>
        </div>
        <div style="padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.05);">
            <p style="color:#94a3b8; font-size:0.9rem; margin-bottom:5px;">DIND SANDBOXES</p>
            <p style="font-size:1.2rem; font-weight:600; color:#10b981;">0 Active / Idle</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-panel">
        <h3>📦 GitHub Kanban</h3>
        <p style="color:#94a3b8; font-size:0.9rem; margin-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:5px;">IN PROGRESS / TO DO</p>
    """, unsafe_allow_html=True)
    
    open_issues = [i for i in issues if i.get("state") == "OPEN"]
    if not open_issues:
        st.markdown("<p style='color:#64748b; font-style:italic; font-size:0.9rem;'>No active tasks.</p>", unsafe_allow_html=True)
    for iss in open_issues:
        st.markdown(f"""
        <div class="kanban-card status-open">
            <span class="issue-id">#{iss['number']}</span>
            <div class="issue-title">{iss['title']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <p style="color:#94a3b8; font-size:0.9rem; margin-top:25px; margin-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:5px;">DONE</p>
    """, unsafe_allow_html=True)
    
    closed_issues = [i for i in issues if i.get("state") == "CLOSED"]
    if not closed_issues:
        st.markdown("<p style='color:#64748b; font-style:italic; font-size:0.9rem;'>No finished tasks yet.</p>", unsafe_allow_html=True)
    for iss in closed_issues:
        st.markdown(f"""
        <div class="kanban-card status-closed">
            <span class="issue-id">#{iss['number']}</span>
            <div class="issue-title">{iss['title']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-panel" style="padding: 0; overflow: hidden;">
        <div class="terminal-container">
            <div class="terminal-header">
                <div class="mac-btn close"></div>
                <div class="mac-btn min"></div>
                <div class="mac-btn max"></div>
                <span style="margin-left: 10px; color: #888; font-size: 0.85rem; font-family: sans-serif;">sandbox-dind-manager ~ root</span>
            </div>
            <div class="terminal-body">
> [DinD Manager] Telemetry Service Booted. 
> Daemon Socket Connected (docker.sock).
> System Ready.
> Waiting for Developer Node to inject /tdd tests into Alpine container...
> ...
> ...
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh simples
time.sleep(4)
st.rerun()
