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

# 2. Premium Cyber Dark Theme CSS Engine
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

# Top Live Statistics Dashboard (Flattened metrics to avoid line break syntax errors)
active_
