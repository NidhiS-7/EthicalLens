import streamlit as st
import google.generativeai as genai
import pdfplumber
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
API_KEY = st.secrets.get("API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Missing GEMINI_API_KEY in .env")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- DYNAMIC MODEL SELECTION ---
@st.cache_resource
def load_model():
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Prioritize 1.5 Flash for speed
    flash_models = [m for m in models if '1.5-flash' in m]
    return genai.GenerativeModel(flash_models[0] if flash_models else models[0])

model = load_model()

# --- DEEP SPACE DARK UI ---
st.set_page_config(page_title="EthicalLens AI", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #05070a;
        color: #e6edf3;
    }
    .main-card {
        background: #0d1117;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        margin-bottom: 25px;
    }
    .stButton>button {
        background: #1f6feb;
        color: white;
        border: none;
        padding: 14px;
        border-radius: 10px;
        font-weight: 700;
        width: 100%;
        transition: 0.2s;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stButton>button:hover {
        background: #388bfd;
        box-shadow: 0 0 15px rgba(31, 111, 235, 0.4);
        color: white;
    }
    textarea { background-color: #010409 !important; color: #f0f6fc !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
    label { color: #8b949e !important; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; }
    
    /* Audit Result Section */
    .report-box {
        background: #161b22;
        border-left: 4px solid #1f6feb;
        padding: 20px;
        border-radius: 0 12px 12px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-card"><h1 style="margin:0; color:#58a6ff;">⚖️ EthicalLens</h1><p style="color:#8b949e; margin-top:5px;">Systemic Bias Auditing | Solution Challenge 2026</p></div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("### 📋 Job Context")
    job_desc = st.text_area("Hiring Criteria:", height=280, placeholder="Paste requirements here...")

with c2:
    st.markdown("### 📄 Candidate File")
    st.write("Upload a PDF resume for cross-analysis.")
    uploaded_file = st.file_uploader("Drop PDF here", type="pdf")

st.markdown("<br>", unsafe_allow_html=True)

# --- ACTION ---
if st.button("🚀 EXECUTE ETHICAL AUDIT"):
    if job_desc and uploaded_file:
        with st.spinner("AI is scanning for bias patterns..."):
            try:
                # 1. Text Extraction
                with pdfplumber.open(uploaded_file) as pdf:
                    text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                
                # 2. Generate content
                prompt = f"Perform an Unconscious Bias Audit:\n\nJOB: {job_desc}\n\nRESUME: {text}\n\nProvide: 1. Fairness Score (0-100), 2. Detailed Bias Flags, 3. Improvement Steps."
                response = model.generate_content(prompt)
                
                # 3. UI Result
                st.balloons()
                st.markdown("---")
                st.markdown(f'<div class="report-box"><h3>📊 Audit Report</h3>{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"⚠️ Service Error: {str(e)}")
                st.info("Tip: Try checking your API key or running 'pip install -U google-generativeai'")
    else:
        st.warning("Both Job Description and Resume are required for a valid audit.")

st.markdown("<br><center><p style='color:#484f58; font-size:0.8rem;'>Project for UN SDG 10: Reduced Inequalities</p></center>", unsafe_allow_html=True)
