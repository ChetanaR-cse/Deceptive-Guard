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

# 2. Premium Cyber Dark Theme CSS Engine (Single-line sanitized string)
css_code = "<style>@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap'); html, body, .stApp { background-color: #030712 !important; color: #f8fafc !important; font-family: 'Plus Jakarta Sans', system-ui, sans-serif; } p, span, label, li, div { color: #e2e8f0 !important; font-size: 16px !important; line-height: 1.8 !important; } h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important; color: #ffffff !important; letter-spacing: -0.01em; } .block-container { position: relative; z-index: 1; max-width: 1250px; padding-top: 1.5rem; padding-bottom: 4rem; margin: 0 auto; } [data-testid='stSidebar'] { background-color: #060911 !important; border-right: 1px solid #1e293b !important; z-index: 2; } .hero-container { background: linear-gradient(135deg, rgba(11, 19, 43, 0.9) 0%, rgba(3, 7, 18, 0.95) 100%); backdrop-filter: blur(12px); border: 1px solid #1e293b; border-left: 6px solid #00f2fe; padding: 32px; border-radius: 18px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(0, 242, 254, 0.15); margin-bottom: 25px; } .badge-tag { background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: #030712 !important; padding: 6px 16px; border-radius: 20px; font-size: 12px !important; font-weight: 800 !important; text-transform: uppercase; letter-spacing: 0.08em; } .metric-card { background: rgba(11, 17, 32, 0.85); backdrop-filter: blur(8px); border: 1px solid #1e293b; border-radius: 14px; padding: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); } .metric-val { font-size: 1.9rem !important; font-weight: 800 !important; color: #00f2fe !important; font-family: 'JetBrains Mono', monospace; } .metric-lbl { font-size: 0.85rem !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.05em; } .stButton > button { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important; color: #ffffff !important; border-radius: 12px !important; padding: 1rem 2.5rem !important; font-weight: 800 !important; font-size: 1.15rem !important; border: none !important; width: 100% !important; box-shadow: 0 4px 25px rgba(0, 114, 255, 0.4) !important; transition: all 0.3s ease-in-out !important; } .stButton > button:hover { background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important; box-shadow: 0 0 30px rgba(0, 198, 255, 0.8) !important; transform: translateY(-2px); } [data-testid='stFileUploader'] { background-color: rgba(11, 17, 32, 0.8) !important; border: 2px dashed #1e293b !important; border-radius: 14px !important; padding: 20px !important; } .stTabs [data-baseweb='tab-list'] { gap: 10px; background-color: #0b1120; padding: 8px; border-radius: 12px; border: 1px solid #1e293b; } .stTabs [data-baseweb='tab'] { height: 48px; border-radius: 8px; color: #94a3b8 !important; font-weight: 700 !important; font-size: 15px !important; } .stTabs [aria-selected='true'] { background-color: #1e293b !important; color: #00f2fe !important; } .card-risk { background: rgba(11, 17, 32, 0.9); border-left: 6px solid #ef4444; border: 1px solid #1e293b; padding: 28px; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(239, 68, 68, 0.15); } .card-tricks { background: rgba(11, 17, 32, 0.9); border-left: 6px solid #38bdf8; border: 1px solid #1e293b; padding: 28px; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(56, 189, 248, 0.15); } .card-laws { background: rgba(11, 17, 32, 0.9); border-left: 6px solid #a855f7; border: 1px solid #1e293b; padding: 28px; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(168, 85, 247, 0.15); } .card-complaint { background: rgba(11, 17, 32, 0.9); border-left: 6px solid #4ade80; border: 1px solid #1e293b; padding: 28px; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(74, 222, 128, 0.15); } .section-title { font-size: 1.35rem !important; font-weight: 800 !important; margin-bottom: 14px; display: flex; align-items: center; gap: 10px; font-family: 'Plus Jakarta Sans', sans-serif; }</style>"
st.markdown(css_code, unsafe_allow_html=True)

# Initialize Session Scan History
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/color/96/cyber-security.png", width=60)
    st.title("Deceptive-Guard")
    st.caption("Multimodal Dark Pattern Sentinel v6.0")
    st.markdown("---")

    st.subheader("⚙️ Regional Scan Controls")

    region_choice = st.selectbox(
        "📍 Regulatory Ruleset Jurisdiction",
        options=[
            "🇮🇳 India (CCPA 2023 Dark Pattern Guidelines & CPA 2019)",
            "🇺🇸 USA (FTC Act Sec 5 & ROSCA Directives)",
            "🇪🇺 European Union (EU Digital Services Act & GDPR)",
            "🇬🇧 United Kingdom (CMA Consumer Protection Regulations)",
            "🌐 Global / Universal Consumer Protection Standard",
        ],
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
    st.info("⚡ Real-time Threat Scanner Ready")

    if st.session_state.scan_history:
        st.markdown("---")
        st.markdown("### 📊 Session History Log")
        for idx, scan_item in enumerate(reversed(st.session_state.scan_history)):
            st.caption(f"Scan #{len(st.session_state.scan_history)-idx}: {scan_item}")

# Hero Header Banner
hero_html = "<div class='hero-container'><span class='badge-tag'>Track 1 - PS 01 | Google Gemma Challenge</span><h1 style='color: #ffffff; font-size: 2.6rem; font-weight: 800; margin-top: 14px; margin-bottom: 6px; letter-spacing: -0.02em;'>🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel</h1><p style='color: #94a3b8; font-size: 1.15rem; margin: 0; line-height: 1.6;'>Detect manipulative checkout traps, hidden pre-checked fees, fake countdown timers, and regulatory compliance breaches instantly using Google Gemma.</p></div>"
st.markdown(hero_html, unsafe_allow_html=True)

# Top Live Statistics Dashboard
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
        f'<div class="metric-card"><div class="metric-val">{region_choice.split()[0]}</div><div class="metric-lbl">Active Ruleset</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val">{len(st.session_state.scan_history)}</div><div class="metric-lbl">Scans Conducted</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Intake Section
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
                pass

        if not active_key:
            st.error("⚠️ Authentication Error: Please enter your Gemini API Key in the sidebar settings.")
        else:
            with st.spinner(f"Analyzing pixels against {region_choice.split('(')[0]} laws in {target_lang}..."):
                try:
                    client = genai.Client(api_key=active_key)

                    prompt = f"You are Deceptive-Guard, an elite consumer protection AI powered by Google Gemma. Analyze this screenshot for online deceptive practices, hidden fees, pre-checked boxes, fake urgency countdowns, or subscription traps.\n\nCONFIGURATION RULES:\n- Target Jurisdiction Rules: Enforce regulatory policies and laws applicable in: {region_choice}.\n- Target Output Language: Provide the entire response in: {target_lang}.\n\nFormat your response strictly using these four exact styled HTML card sections:\n\nSECTION 1:\n<div class=\"card-risk\"><div class=\"section-title\" style=\"color: #f87171;\">🚨 SCAM RISK SCORE</div><div style=\"font-size: 38px; font-weight: 800; color: #ef4444; margin-top: 5px; font-family: 'JetBrains Mono', monospace;\">[State Percentage, e.g., 75% - HIGH RISK]</div><div style=\"background: #1e293b; border-radius: 10px; height: 12px; width: 100%; margin-top: 15px; overflow: hidden;\"><div style=\"background: linear-gradient(90deg, #f59e0b 0%, #ef4444 100%); height: 100%; width: 75%; border-radius: 10px;\"></div></div></div>\n\nSECTION 2:\n<div class=\"card-tricks\"><div class=\"section-title\" style=\"color: #38bdf8;\">🔍 DECEPTIVE TRICKS IDENTIFIED</div><div style=\"color: #f1f5f9; font-size: 16px; line-height: 1.8;\">[Provide bulleted points detailing dark patterns found in {target_lang}]</div></div>\n\nSECTION 3:\n<div class=\"card-laws\"><div class=\"section-title\" style=\"color: #c084fc;\">⚖️ SPECIFIC LEGAL & REGULATORY VIOLATIONS</div><div style=\"color: #f1f5f9; font-size: 16px; line-height: 1.8;\">[Explicitly name laws or guidelines breached under {region_choice} in {target_lang}]</div></div>\n\nSECTION 4:\n<div class=\"card-complaint\"><div class=\"section-title\" style=\"color: #4ade80;\">📝 READY-TO-FILE COMPLAINT LETTER</div><div style=\"color: #e2e8f0; font-size: 16px; line-height: 1.8;\">[Provide a formal ready-to-copy grievance letter in {target_lang}]</div></div>"

                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it
