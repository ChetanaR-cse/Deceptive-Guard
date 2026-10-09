import io
from PIL import Image
from google import genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Deceptive-Guard | Enterprise Dark Pattern Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Advanced Cyber Dark Theme CSS Engine
st.markdown(
    """
    <style>
    /* Global Base & Animated Grid Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, .stApp {
        background-color: #05070e !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 242, 254, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(112, 0, 255, 0.08) 0px, transparent 50%);
        color: #f1f5f9 !important;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    /* Text & Header Global Visibility */
    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #e2e8f0;
    }

    /* Main Container Padding */
    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        margin: 0 auto;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #070a12 !important;
        border-right: 1px solid #1e293b !important;
    }

    /* Hero Banner Styling with Neon Glow */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #090e1a 100%);
        border: 1px solid #1e293b;
        border-left: 6px solid #00f2fe;
        padding: 32px;
        border-radius: 18px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 25px rgba(0, 242, 254, 0.15);
        margin-bottom: 25px;
    }

    .badge-tag {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: #030712 !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Cyber Metric Cards */
    .metric-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #00f2fe;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Primary Action Button Glow */
    .stButton > button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 25px rgba(0, 114, 255, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
        letter-spacing: 0.03em;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important;
        box-shadow: 0 0 30px rgba(0, 198, 255, 0.8) !important;
        transform: translateY(-2px);
    }

    /* Custom File Uploader Zone */
    [data-testid="stFileUploader"] {
        background-color: #0b1120 !important;
        border: 2px dashed #1e293b !important;
        border-radius: 14px !important;
        padding: 18px !important;
    }

    /* Streamlit Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #0b1120;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1e293b;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #00f2fe !important;
    }

    /* Styled Audit Report Cards */
    .card-risk {
        background: #0f172a;
        border-left: 6px solid #ef4444;
        border: 1px solid #1e293b;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15);
    }
    .card-tricks {
        background: #0f172a;
        border-left: 6px solid #38bdf8;
        border: 1px solid #1e293b;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.15);
    }
    .card-laws {
        background: #0f172a;
        border-left: 6px solid #a855f7;
        border: 1px solid #1e293b;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.15);
    }
    .card-complaint {
        background: #0f172a;
        border-left: 6px solid #4ade80;
        border: 1px solid #1e293b;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(74, 222, 128, 0.15);
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session History
if "scan_history" not in st.session_state:
  st.session_state.scan_history = []

# Sidebar Controls
with st.sidebar:
  st.image("https://img.icons8.com/color/96/cyber-security.png", width=60)
  st.title("Deceptive-Guard")
  st.caption("Multimodal Dark Pattern Sentinel v3.0")
  st.markdown("---")

  st.subheader("⚙️ Regional Scan Controls")

  # Jurisdiction Selector
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

  # Multilingual Language Selector
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
  st.info("⚡ Multimodal Threat Scanner Ready")

  if st.session_state.scan_history:
    st.markdown("---")
    st.markdown("### 📊 Session History Log")
    for idx, scan_item in enumerate(reversed(st.session_state.scan_history)):
      st.caption(f"Scan #{len(st.session_state.scan_history)-idx}: {scan_item}")

# Hero Header Banner
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-tag">Track 1 - PS 01 | Google Gemma Challenge</span>
        <h1 style="color: #ffffff; font-size: 2.5rem; font-weight: 800; margin-top: 12px; margin-bottom: 6px; letter-spacing: -0.02em;">
            🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem; margin: 0; line-height: 1.5;">
            Detect manipulative checkout traps, hidden pre-checked fees, fake countdown timers, and regulatory compliance breaches instantly using Google Gemma.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

# Top Live Statistics Dashboard
m1, m2, m3, m4 = st.columns(4)
with m1:
  st.markdown(
      '<div class="metric-card"><div'
      ' class="metric-val">gemma-4-26b</div><div class="metric-lbl">AI Core'
      " Engine</div></div>",
      unsafe_allow_html=True,
  )
with m2:
  st.markdown(
      '<div class="metric-card"><div class="metric-val">< 2.2s</div><div'
      ' class="metric-lbl">Avg Scan Latency</div></div>',
      unsafe_allow_html=True,
  )
with m3:
  st.markdown(
      f'<div class="metric-card"><div'
      f' class="metric-val">{region_choice.split()[0]}</div><div'
      ' class="metric-lbl">Active Ruleset</div></div>',
      unsafe_allow_html=True,
  )
with m4:
  st.markdown(
      f'<div class="metric-card"><div'
      f' class="metric-val">{len(st.session_state.scan_history)}</div><div'
      ' class="metric-lbl">Scans Conducted</div></div>',
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
      "Drop
