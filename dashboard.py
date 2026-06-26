import streamlit as st
import time

st.set_page_config(page_title="Agent Forge", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global styling */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
        background-color: #0b0f19 !important;
        color: #e2e8f0 !important;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Title */
    h1 {
        font-weight: 800;
        background: linear-gradient(90deg, #8b5cf6, #3b82f6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 3.5rem !important;
    }

    p.subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 3rem;
    }

    /* Text Input */
    .stTextInput>div>div>input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        padding: 15px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4) !important;
    }

    /* Primary Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 0 !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
        cursor: pointer;
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
    }

    .stButton>button:active {
        transform: translateY(1px) scale(0.98) !important;
    }

    /* Kanban Columns */
    .kanban-col {
        background: #1e293b;
        border-radius: 16px;
        padding: 20px;
        min-height: 400px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid #334155;
        transition: all 0.4s ease;
    }
    
    .kanban-col:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        border-color: #475569;
    }

    .col-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .todo-title { color: #cbd5e1; }
    .prog-title { color: #60a5fa; }
    .done-title { color: #34d399; }

    /* Task Cards */
    .task-card {
        background: #0f172a;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #334155;
        position: relative;
        overflow: hidden;
        animation: slideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .task-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
    }

    .todo-card::before { background: #94a3b8; }
    .prog-card::before { background: #3b82f6; }
    .done-card::before { background: #10b981; }

    .task-title {
        font-weight: 600;
        margin-bottom: 5px;
        color: #f1f5f9;
    }

    .task-desc {
        font-size: 0.85rem;
        color: #94a3b8;
    }
    
    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .pulse-dot {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
    }
    
    .pulse-prog {
        background-color: #3b82f6;
        box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
        animation: pulse-blue 2s infinite;
    }

    @keyframes pulse-blue {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Agent Forge</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The Autonomous Software Factory of the Future</p>", unsafe_allow_html=True)

# Input area
col_input, col_btn = st.columns([3, 1])

with col_input:
    ideia = st.text_input("Your Idea", placeholder="Describe what Agent Forge should build...", label_visibility="collapsed")

with col_btn:
    executar = st.button("Run Factory")

if executar and ideia:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    # Simulate To Do
    with c1:
        st.markdown('''
        <div class="kanban-col">
            <div class="col-title todo-title">📋 To Do</div>
            <div class="task-card todo-card">
                <div class="task-title">Deploy App</div>
                <div class="task-desc">Publish to AWS cloud</div>
            </div>
            <div class="task-card todo-card">
                <div class="task-title">E2E Tests</div>
                <div class="task-desc">Validate user flows</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    # Simulate In Progress
    with c2:
        safe_ideia = ideia.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        short_ideia = safe_ideia[:30] + '...' if len(safe_ideia) > 30 else safe_ideia
        
        st.markdown(f'''
        <div class="kanban-col">
            <div class="col-title prog-title"><span class="pulse-dot pulse-prog"></span> In Progress</div>
            <div class="task-card prog-card">
                <div class="task-title">Analyze Requirements</div>
                <div class="task-desc">Processing the idea: "{short_ideia}"</div>
            </div>
            <div class="task-card prog-card">
                <div class="task-title">Generate Backend</div>
                <div class="task-desc">Building FastAPI routes</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    # Simulate Done
    with c3:
        st.markdown('''
        <div class="kanban-col">
            <div class="col-title done-title">✨ Done</div>
            <div class="task-card done-card">
                <div class="task-title">Repository Setup</div>
                <div class="task-desc">Initial structure created successfully</div>
            </div>
            <div class="task-card done-card">
                <div class="task-title">Configure CI/CD</div>
                <div class="task-desc">Github Actions ready</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.toast("Factory started successfully! Simulation in progress...", icon="🚀")

elif executar and not ideia:
    st.warning("Please type an idea before running the factory.")
