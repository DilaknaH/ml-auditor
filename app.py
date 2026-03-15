import streamlit as st
from ml_auditor.engine import AuditorEngine
from ml_auditor.reporter import generate_pdf_report
from ml_auditor.llm.chatbot import chat_with_assistant
import tempfile
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ML Auditor Pro",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'results' not in st.session_state:
    st.session_state.results = None
if 'code_content' not in st.session_state:
    st.session_state.code_content = ""
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- THEME CSS (Ocean Blue + UI Polish) ---
st.markdown("""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}

    /* Main Background */
    html, body, [class*="css"] {
        background-color: #03045e;
        color: #caf0f8;
    }

    /* Navigation Bar */
    .navbar {
        background-color: #023e8a;
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 30px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0077b6;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00b4d8;
        color: white;
    }
    .stButton>button[kind="primary"] {
        background-color: #00b4d8;
        color: #03045e;
        font-weight: bold;
    }

    /* Left AI ASSIST Button */
    .ai-button {
        position: fixed;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 9999;
    }
    .ai-button button {
        width: 170px;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #023e8a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #caf0f8 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #023e8a;
        color: #caf0f8 !important;
    }
    
    /* File Uploader */
    section[data-testid="stFileUploader"] {
        background-color: #023e8a;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #0077b6;
    }
    
    /* Chat Input Fixes */
    div[data-testid="stChatInput"], 
    section[data-testid="stChatInput"], 
    div[data-testid="stChatInput"] > div, 
    section[data-testid="stChatInput"] > div {
        border-top: 0px !important;
        border: none !important;
        box-shadow: none !important;
        background-color: #023e8a !important;
    }

    .stChatInput textarea {
        background-color: #023e8a !important;
        color: white !important;
        border: 1px solid #0077b6 !important;
    }
    
    /* Home Page Specific */
    .welcome-banner {
        background-color: #0077b6;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
    }
    .step-card {
        background-color: #023e8a;
        padding: 20px;
        border-radius: 10px;
        height: 100%;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: API KEY INPUT ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.text_input("OpenAI API Key", type="password", key="api_key_input", value=st.session_state.api_key, help="Required for AI Fixes")
    if st.session_state.api_key_input != st.session_state.api_key:
        st.session_state.api_key = st.session_state.api_key_input
    
    st.markdown("---")
    st.caption("ML Auditor Pro v2.0")

# --- NAVIGATION BAR ---
def render_nav():
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    
    with col1:
        st.markdown("### 🛡️ ML Auditor Pro")
    
    with col2:
        if st.button(" Home"):
            st.session_state.page = "home"
            st.rerun()
    
    with col3:
        if st.button("Auditor"):
            st.session_state.page = "auditor"
            st.rerun()
    
    with col4:
        if st.session_state.results:
            if st.button(" Reset"):
                st.session_state.results = None
                st.session_state.code_content = ""
                st.session_state.messages = []
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)

render_nav()

# --- LEFT AI ASSIST BUTTON ---
st.markdown('<div class="ai-button">', unsafe_allow_html=True)
if st.button(" AI ASSIST"):
    st.session_state.page = "chat"
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --------------------
# HOME PAGE
# --------------------
if st.session_state.page == "home":
    
    # 1. WELCOME BANNER
    st.markdown("""
    <div class="welcome-banner">
        <h1>Welcome to ML Auditor Pro</h1>
        <p style="font-size: 1.2em; color: #caf0f8;">Your Personal Machine Learning Quality Assurance Tool</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. PROJECT DEFINITION
    st.markdown("###  What is this tool?")
    st.write("""
    **ML Auditor Pro** is an open source static analysis tool designed specifically for Machine Learning code. 
    Unlike standard linters that check for syntax errors, we detect **silent logic bugs** critical mistakes 
    like **Data Leakage**, **Metric Misuse**, and **Reproducibility issues** that ruin models but don't crash code.
    """)
    st.write("---")

    # 3. HOW TO USE (Step-by-Step Guide)
    st.markdown("###  How to Use")
    st.write("Follow these simple steps to audit your ML code:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="step-card">
            <h2>1. Upload Code</h2>
            <p>Navigate to the <b>Auditor Tool</b> tab. Drag and drop your <code>.py</code> or Jupyter <code>.ipynb</code> file.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="step-card">
            <h2>2. Run Audit</h2>
            <p>Click the <b>"Run Audit"</b> button. The engine will parse your code structure using AST analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="step-card">
            <h2>3. Fix & Report</h2>
            <p>Review the Health Score, fix bugs with AI help, and download a <b>PDF Report</b> for compliance.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 4. KEY FEATURES
    st.markdown("### Key Features")
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.info(" **Flexible Input**\n\nSupports standard Python scripts and Jupyter Notebooks.")
    
    with feature_col2:
        st.success("**Hybrid AI Engine**\n\nWorks offline (Static Analysis) and online (GPT Fixes).")

    with feature_col3:
        st.warning("**Compliance Ready**\n\nGenerate professional PDF audit trails for reports.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # CALL TO ACTION
    if st.button("Start Auditing Now", type="primary"):
        st.session_state.page = "auditor"
        st.rerun()

# --------------------
# AUDITOR PAGE
# --------------------
elif st.session_state.page == "auditor":
    st.header("Audit Dashboard")
    
    if st.session_state.results:
        results = st.session_state.results
        col1, col2 = st.columns([1, 3])
        
        with col1:
            score = results['score']
            score_color = "#00b4d8"
            
            st.markdown(f"""
            <div style="text-align:center; padding:30px; background-color:{score_color}; border-radius:10px;">
                <h1 style="margin:0; font-size:3em; color:#03045e;">{score}</h1>
                <p style="font-size:1.2em; color:#03045e;">Health Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if not results['issues']:
                st.success("✅ No critical issues found.")
            else:
                st.warning(f"Found {len(results['issues'])} issue(s).")

        if results['issues']:
            st.markdown("---")
            for i, issue in enumerate(results['issues']):
                title = f"⚠️ Issue #{i+1}: {issue.get('type')} (Line {issue.get('line')})"
                with st.expander(title, expanded=(i==0)):
                    st.markdown(f"**Severity:** `{issue.get('severity')}`")
                    st.markdown(f"**Message:** {issue.get('message')}")
                    
                    if 'snippet' in issue:
                        st.code(issue['snippet'], language='python')
                    
                    if 'fixed_code' in issue and issue['fixed_code']:
                        st.markdown("#### 🤖 AI Generated Fix:")
                        st.code(issue['fixed_code'], language='python')
                        st.download_button("Download Fix", issue['fixed_code'], file_name="fixed_code.py")
        
        st.markdown("---")
        try:
            pdf_path = generate_pdf_report(results)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF Audit Report",
                    data=f,
                    file_name="ML_Audit_Report.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"PDF Generation Failed: {e}")

        if st.button("Start New Audit", type="primary", key="reset_main"):
            st.session_state.results = None
            st.session_state.code_content = ""
            st.session_state.messages = []
            st.rerun()

    else:
        uploaded_file = st.file_uploader("Drop your .py or .ipynb file here", type=["py", "ipynb"])
        
        if uploaded_file:
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            
            try:
                st.session_state.code_content = uploaded_file.getvalue().decode("utf-8")
            except:
                st.session_state.code_content = "Binary content"

            if st.button("Run Audit", type="primary"):
                with st.spinner("Analyzing AST structure..."):
                    engine = AuditorEngine(tmp_path)
                    results = engine.run_audit(api_key=st.session_state.api_key if st.session_state.api_key else None)
                    st.session_state.results = results
                st.rerun()

# --------------------
# AI ASSIST PAGE
# --------------------
elif st.session_state.page == "chat":
    col1, col2 = st.columns([8, 2])
    with col1:
        st.header("AI ASSIST")
    with col2:
        if st.button("⬅ Back"):
            st.session_state.page = "auditor"
            st.rerun()
    
    # Status Message
    if not st.session_state.code_content:
        st.info("Please upload a file in the Auditor Tool first.")
    elif not st.session_state.api_key:
        st.info("**Offline Mode** | File loaded. Use buttons or type below.")
    else:
        st.success("**Online AI Mode** | File loaded.")

    # --- QUICK ACTION BUTTONS ---
    if st.session_state.code_content:
        st.markdown("## Suggested Questions")
        b1, b2, b3, b4 = st.columns(4)
        
        with b1:
            if st.button("Summary"):
                user_query = "Summary of issues found"
                st.session_state.messages.append({"role": "user", "content": user_query})
                resp = chat_with_assistant(user_query, st.session_state.code_content, st.session_state.api_key, st.session_state.results)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.rerun()

        with b2:
            if st.button("How to Fix"):
                user_query = "How to fix code"
                st.session_state.messages.append({"role": "user", "content": user_query})
                resp = chat_with_assistant(user_query, st.session_state.code_content, st.session_state.api_key, st.session_state.results)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.rerun()

        with b3:
            if st.button("Leakage"):
                user_query = "Explain leakage"
                st.session_state.messages.append({"role": "user", "content": user_query})
                resp = chat_with_assistant(user_query, st.session_state.code_content, st.session_state.api_key, st.session_state.results)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.rerun()
        
        with b4:
            if st.button("Overfitting"):
                user_query = "Explain overfitting"
                st.session_state.messages.append({"role": "user", "content": user_query})
                resp = chat_with_assistant(user_query, st.session_state.code_content, st.session_state.api_key, st.session_state.results)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.rerun()

        st.markdown("---")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask about your ML code..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            response = chat_with_assistant(
                prompt,
                st.session_state.code_content,
                st.session_state.api_key,
                audit_results=st.session_state.results
            )
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
