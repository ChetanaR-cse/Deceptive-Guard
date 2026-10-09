import io
import re
from PIL import Image
from google import genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Deceptive-Guard | AI Dark Pattern Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CSS Engine - Built via list.append to completely prevent paste auto-wrap errors
css_list = []
css_list.append("<style>")
css_list.append("@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap');")
css_list.append("html, body, .stApp {")
css_list.append("    background-color: #030712 !important;")
css_list.append("    background-image: radial-gradient(at 0% 0%, rgba(0, 242, 254, 0.15) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(124, 58, 237, 0.15) 0px, transparent 50%) !important;")
css_list.append("    color: #f8fafc !important;")
css_list.append("    font-family: 'Plus Jakarta Sans', sans-serif;")
css_list.append("}")
css_list.append("p, span, label, li, div {")
css_list.append("    color: #e2e8f0 !important;")
css_list.append("    font-size: 16px !important;")
css_list.append("    line-height: 1.8 !important;")
css_list.append("}")
css_list.append("h1 {")
css_list.append("    font-family: 'Plus Jakarta Sans', sans-serif !important;")
css_list.append("    font-weight: 800 !important;")
css_list.append("    color: #00f2fe !important;")
css_list.append("    letter-spacing: -0.01em;")
css_list.append("}")
css_list.append("h2, h3 {")
css_list.append("    font-family: 'Plus Jakarta Sans', sans-serif !important;")
css_list.append("    font-weight: 800 !important;")
css_list.append("    color: #38bdf8 !important;")
css_list.append("    letter-spacing: -0.01em;")
css_list.append("}")
css_list.append("h4, h5, h6 {")
css_list.append("    font-family: 'Plus Jakarta Sans', sans-serif !important;")
css_list.append("    font-weight: 700 !important;")
css_list.append("    color: #fbbf24 !important;")
css_list.append("}")
css_list.append(".block-container {")
css_list.append("    position: relative;")
css_list.append("    z-index: 1;")
css_list.append("    max-width: 1250px;")
css_list.append("    padding-top: 1.5rem;")
css_list.append("    padding-bottom: 4rem;")
css_list.append("    margin: 0 auto;")
css_list.append("}")
css_list.append("[data-testid='stSidebar'] {")
css_list.append("    background-color: rgba(6, 9, 17, 0.95) !important;")
css_list.append("    border-right: 1px solid #1e293b !important;")
css_list.append("    backdrop-filter: blur(12px);")
css_list.append("    z-index: 2;")
css_list.append("}")
css_list.append(".hero-container {")
css_list.append("    background: rgba(11, 17, 32, 0.85);")
css_list.append("    backdrop-filter: blur(16px);")
css_list.append("    border: 1px solid rgba(0, 242, 254, 0.4);")
css_list.append("    border-left: 6px solid #00f2fe;")
css_list.append("    padding: 32px;")
css_list.append("    border-radius: 18px;")
css_list.append("    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(0, 242, 254, 0.2);")
css_list.append("    margin-bottom: 25px;")
css_list.append("}")
css_list.append(".badge-tag {")
css_list.append("    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);")
css_list.append("    color: #030712 !important;")
css_list.append("    padding: 6px 16px;")
css_list.append("    border-radius: 20px;")
css_list.append("    font-size: 12px !important;")
css_list.append("    font-weight: 800 !important;")
css_list.append("    text-transform: uppercase;")
css_list.append("    letter-spacing: 0.08em;")
css_list.append("}")
css_list.append(".metric-card {")
css_list.append("    background: rgba(15, 23, 42, 0.85);")
css_list.append("    backdrop-filter: blur(12px);")
css_list.append("    border: 1px solid #1e293b;")
css_list.append("    border-radius: 14px;")
css_list.append("    padding: 20px;")
css_list.append("    text-align: center;")
css_list.append("    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);")
css_list.append("}")
css_list.append(".metric-val {")
css_list.append("    font-size: 1.9rem !important;")
css_list.append("    font-weight: 800 !important;")
css_list.append("    color: #00f2fe !important;")
css_list.append("    font-family: 'JetBrains Mono', monospace;")
css_list.append("}")
css_list.append(".metric-lbl {")
css_list.append("    font-size: 0.85rem !important;")
css_list.append("    color: #fbbf24 !important;")
css_list.append("    text-transform: uppercase;")
css_list.append("    letter-spacing: 0.05em;")
css_list.append("    font-weight: 700 !important;")
css_list.append("}")
css_list.append(".stButton > button {")
css_list.append("    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;")
css_list.append("    color: #ffffff !important;")
css_list.append("    border-radius: 12px !important;")
css_list.append("    padding: 1rem 2.5rem !important;")
css_list.append("    font-weight: 800 !important;")
css_list.append("    font-size: 1.15rem !important;")
css_list.append("    border: none !important;")
css_list.append("    width: 100% !important;")
css_list.append("    box-shadow: 0 4px 25px rgba(0, 114, 255, 0.4) !important;")
css_list.append("    transition: all 0.3s ease-in-out !important;")
css_list.append("}")
css_list.append(".stButton > button:hover {")
css_list.append("    background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important;")
css_list.append("    box-shadow: 0 0 30px rgba(0, 198, 255, 0.8) !important;")
css_list.append("    transform: translateY(-2px);")
css_list.append("}")
css_list.append("[data-testid='stFileUploader'] {")
css_list.append("    background-color: rgba(15, 23, 42, 0.8) !important;")
css_list.append("    border: 2px dashed #00f2fe !important;")
css_list.append("    border-radius: 14px !important;")
css_list.append("    padding: 20px !important;")
css_list.append("}")
css_list.append(".stTabs [data-baseweb='tab-list'] {")
css_list.append("    gap: 10px;")
css_list.append("    background-color: rgba(11, 17, 32, 0.9);")
css_list.append("    padding: 8px;")
css_list.append("    border-radius: 12px;")
css_list.append("    border: 1px solid #1e293b;")
css_list.append("}")
css_list.append(".stTabs [data-baseweb='tab'] {")
css_list.append("    height: 48px;")
css_list.append("    border-radius: 8px;")
css_list.append("    color: #94a3b8 !important;")
css_list.append("    font-weight: 700 !important;")
css_list.append("    font-size: 15px !important;")
css_list.append("}")
css_list.append(".stTabs [aria-selected='true'] {")
css_list.append("    background-color: #1e293b !important;")
css_list.append("    color: #00f2fe !important;")
css_list.append("}")
css_list.append("</style>")

st.markdown("\n".join(css_list), unsafe_allow_html=True)

# Initialize Session Scan History
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# 3. Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/color/96/cyber-security.png", width=60)
    st.title("Deceptive-Guard")
    st.caption("Multimodal Dark Pattern Sentinel v6.0")
    st.markdown("---")

    st.subheader("⚙️ Regional Scan Controls")

    region_options = [
        "🇮🇳 India (CCPA 2023 Guidelines & CPA 2019)",
        "🇺🇸 USA (FTC Act Sec 5 & ROSCA Directives)",
        "🇪🇺 European Union (EU DSA & GDPR)",
        "🇬🇧 United Kingdom (CMA Regulations)",
        "🌐 Global Consumer Protection Standard",
    ]

    region_choice = st.selectbox(
        "📍 Regulatory Ruleset Jurisdiction",
        options=region_options,
        index=0,
    )

    target_lang = st.selectbox(
        "🌐 Audit Output Language",
        options=[
            "English",
            "Kannada (ಕನ್ನಡ)",
            "Hindi (हिंदी)",
            "Spanish (Español)",
            "French (Français)",
            "German (Deutsch)",
        ],
        index=0,
    )

    st.markdown("---")
    with st.expander("🔐 API Settings"):
        sidebar_key = st.text_input("Gemini API Key", type="password")

    st.markdown("---")
    st.success("🟢 Gemma Vision Engine Online")
    st.info("⚡ Cyber Aurora Background Active")

    if st.session_state.scan_history:
        st.markdown("---")
        st.markdown("### 📊 Session History Log")
        for idx, scan_item in enumerate(reversed(st.session_state.scan_history)):
            st.caption(f"Scan #{len(st.session_state.scan_history)-idx}: {scan_item}")

# 4. Hero Header Banner
hero_list = []
hero_list.append('<div class="hero-container">')
hero_list.append('<span class="badge-tag">Track 1 - PS 01 | Google Gemma Challenge</span>')
hero_list.append('<h1 style="color: #00f2fe !important; font-size: 2.6rem; font-weight: 800; margin-top: 14px; margin-bottom: 6px; letter-spacing: -0.02em;">')
hero_list.append('🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel')
hero_list.append('</h1>')
hero_list.append('<p style="color: #38bdf8 !important; font-size: 1.15rem; margin: 0; line-height: 1.6;">')
hero_list.append('Detect manipulative checkout traps, hidden pre-checked fees, fake countdown timers, and regulatory compliance breaches instantly using Google Gemma.')
hero_list.append('</p>')
hero_list.append('</div>')

st.markdown("\n".join(hero_list), unsafe_allow_html=True)

# Variables derived AFTER sidebar definition
active_flag = region_choice.split()[0]
total_scans = str(len(st.session_state.scan_history))

# 5. Top Live Statistics Dashboard
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        '<div class="metric-card"><div class="metric-val">gemma-4-26b</div><div class="metric-lbl">AI Core Engine</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        '<div class="metric-card"><div class="metric-val">< 2.2s</div><div class="metric-lbl">Avg Scan Latency</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val">{active_flag}</div><div class="metric-lbl">Active Ruleset</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val">{total_scans}</div><div class="metric-lbl">Scans Conducted</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# 6. Intake Section
st.markdown("### 📥 Step 1: Upload Interface Screenshot or Camera Feed")
input_method = st.radio(
    "Choose input method:",
    ["📁 Upload Image File", "📸 Capture via Webcam"],
    horizontal=True,
    label_visibility="collapsed",
)

image = None
if "Upload" in input_method:
    uploaded_file = st.file_uploader(
        "Drop your e-commerce checkout page, cart summary, or booking screenshot here...",
        type=["jpg", "png", "jpeg"],
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
else:
    camera_image = st.camera_input("Capture frame")
    if camera_image:
        image = Image.open(camera_image)

if image is not None:
    st.markdown("---")
    st.subheader("🎯 Target Inspection Frame")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Ingested Target UI Evidence", use_container_width=True)

    st.markdown("---")
    if st.button("🚀 Run Deceptive-Guard Forensic Audit", use_container_width=True):
        active_key = sidebar_key
        if not active_key:
            try:
                active_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                active_key = None

        if not active_key:
            st.error("⚠️ Authentication Error: Please enter your Gemini API Key in the sidebar settings.")
        else:
            with st.spinner("Analyzing pixels against regional consumer laws..."):
                try:
                    client = genai.Client(api_key=active_key)

                    prompt_parts = []
                    prompt_parts.append("You are Deceptive-Guard, an elite consumer protection AI powered by Google Gemma. ")
                    prompt_parts.append("Analyze this screenshot for online deceptive practices, hidden fees, pre-checked boxes, fake urgency countdowns, or subscription traps.\n\n")
                    prompt_parts.append("CONFIGURATION RULES:\n")
                    prompt_parts.append("1. Target Jurisdiction Rules: Enforce policies applicable in: " + str(region_choice) + ".\n")
                    prompt_parts.
