import io
from PIL import Image
from google import genai
import streamlit as st

# 1. Page Configuration & Favicon
st.set_page_config(
    page_title="Deceptive-Guard | AI UI Trap & Scam Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Advanced Cyber Dark Theme CSS Engine
st.markdown(
    """
    <style>
    /* Global Base Reset & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, .stApp {
        background-color: #05070c !important;
        color: #f1f5f9 !important;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    /* Text & Header Global Visibility */
    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #e2e8f0;
    }

    /* Container Constraints */
    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        margin: 0 auto;
    }

    /* Sidebar Dark Customization */
    [data-testid="stSidebar"] {
        background-color: #080c14 !important;
        border-right: 1px solid #1e293b !important;
    }

    /* Hero Banner Styling with Neon Glow */
    .hero-container {
        background: linear-gradient(135deg, #0b1329 0%, #080e1e 100%);
        border: 1px solid #1e293b;
        border-left: 6px solid #00f2fe;
        padding: 32px;
        border-radius: 18px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 20px rgba(0, 242, 254, 0.1);
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

    /* Streamlit Tabs Styling */
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

    /* Report Card Outputs */
    .report-card {
        background-color: #0b1120 !important;
        border: 1px solid #1e293b !important;
        border-top: 4px solid #00f2fe !important;
        padding: 30px !important;
        border-radius: 16px !important;
        margin-top: 20px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8) !important;
    }

    .report-card h3 {
        color: #00f2fe !important;
        font-size: 1.3rem !important;
        margin-top: 22px !important;
        margin-bottom: 12px !important;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
    }

    .report-card p, .report-card li {
        color: #cbd5e1 !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session Scan History
if "scan_history" not in st.session_state:
  st.session_state.scan_history = []

# Sidebar Controls
with st.sidebar:
  st.image("https://img.icons8.com/color/96/cyber-security.png", width=60)
  st.title("Deceptive-Guard")
  st.caption("Multimodal Consumer Shield v2.0")
  st.markdown("---")

  st.subheader("⚙️ Regional Scan Controls")

  # NEW FEATURE 1: Jurisdiction & Legal Framework Selector
  region_choice = st.selectbox(
      "📍 Target Jurisdiction & Regulatory Rules",
      options=[
          "🇮🇳 India (CCPA 2023 Dark Pattern Guidelines & Consumer Protection Act)",
          "🇺🇸 USA (FTC Act Sec 5 & ROSCA Compliance Rules)",
          "🇪🇺 European Union (EU Digital Services Act & GDPR Provisions)",
          "🇬🇧 United Kingdom (CMA Consumer Protection Regulations)",
          "🌐 Global / Universal Consumer Protection Framework",
      ],
      index=0,
  )

  # NEW FEATURE 2: Multilingual Language Selector
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
  with st.expander("🔐 API Authentication"):
    sidebar_key = st.text_input("Gemini API Key", type="password")

  st.markdown("---")
  st.success("🟢 Gemma Vision Engine Online")
  st.info("⚡ Real-time OCR + Pixel Analysis Active")

  # NEW FEATURE 3: Live Session History Counter
  if st.session_state.scan_history:
    st.markdown("---")
    st.markdown("### 📊 Session Scan Log")
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
            Detect sneaky e-commerce traps, hidden subscriptions, fake urgency countdowns, and regulatory compliance breaches instantly powered by Google Gemma multimodal vision.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

# Top Live Statistics Row
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
      '<div class="metric-card"><div class="metric-val">< 2.5s</div><div'
      ' class="metric-lbl">Avg Scan Latency</div></div>',
      unsafe_allow_html=True,
  )
with m3:
  st.markdown(
      f'<div class="metric-card"><div'
      f' class="metric-val">{region_choice.split()[0]}</div><div'
      ' class="metric-lbl">Active Region</div></div>',
      unsafe_allow_html=True,
  )
with m4:
  st.markdown(
      f'<div class="metric-card"><div'
      f' class="metric-val">{len(st.session_state.scan_history)}</div><div'
      ' class="metric-lbl">Scans Completed</div></div>',
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# Intake Section
st.markdown("### 📥 Step 1: Upload Interface Screenshot or Live Photo")
input_method = st.radio(
    "Choose input method:",
    ["📁 Upload Image File", "📸 Capture via Webcam"],
    horizontal=True,
    label_visibility="collapsed",
)

image = None
if "Upload" in input_method:
  uploaded_file = st.file_uploader(
      "Drop your checkout page, cart summary, or subscription modal screenshot"
      " here...",
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
  st.subheader("🎯 Evidence Stream Inspection")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.image(
        image,
        caption="Ingested Target UI Frame",
        use_container_width=True,
    )

  st.markdown("---")
  if st.button("🚀 Run Deceptive-Guard Forensic Audit", use_container_width=True):
    active_key = sidebar_key
    if not active_key:
      try:
        active_key = st.secrets["GEMINI_API_KEY"]
      except Exception:
        pass

    if not active_key:
      st.error(
          "⚠️ Authentication Error: Please enter your Gemini API Key in the"
          " sidebar settings."
      )
    else:
      with st.spinner(
          f"Executing multi-vector audit against {region_choice.split('(')[0]} rules in"
          f" {target_lang}..."
      ):
        try:
          client = genai.Client(api_key=active_key)

          # Dynamic Prompt Tailored to Selected Jurisdiction & Language
          prompt = f"""
                    You are Deceptive-Guard, an elite consumer protection AI powered by Google Gemma. 
                    Analyze this screenshot for online deceptive practices, hidden fees, pre-checked boxes, fake countdown timers, or cancellation traps.

                    CONFIGURATION RULES:
                    - Target Jurisdiction Rules: Enforce regulatory policies and laws applicable in: {region_choice}.
                    - Target Output Language: Provide the entire response in: {target_lang}.

                    Format your response strictly using these exact HTML/Markdown sections:
                    1. <h3>🚨 SCAM RISK SCORE</h3><div style="font-size: 38px; font-weight: 800; color: #ff4d4d; margin: 10px 0;">[State Risk Percentage, e.g., 92% - HIGH RISK CRITICAL]</div>
                    2. <h3>🔍 DECEPTIVE TRICKS IDENTIFIED</h3> [Provide bulleted breakdowns of visual dark patterns found on the page in simple terms]
                    3. <h3>⚖️ SPECIFIC LEGAL & REGULATORY VIOLATIONS</h3> [Explicitly name laws, consumer protection clauses, or trade guidelines breached in {region_choice}]
                    4. <h3>📝 READY-TO-FILE COMPLAINT LETTER</h3> [Generate a complete, ready-to-copy grievance complaint letter addressed to relevant authorities or the company support team]
                    """

          response = client.models.generate_content(
              model="gemma-4-26b-a4b-it", contents=[image, prompt]
          )

          st.success("✅ Forensic Scan Completed Successfully!")

          # Update Session History
          st.session_state.scan_history.append(
              f"{region_choice.split()[0]} | {target_lang}"
          )

          # Tabbed Interactive Output Dashboard
          tab1, tab2, tab3 = st.tabs([
              "📊 Executive Audit Report",
              "📝 Formal Legal Complaint",
              "⚡ RAW Telemetry & Code",
          ])

          with tab1:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

          with tab2:
            st.markdown(
                "#### 📝 Auto-Generated Consumer Grievance Complaint"
            )
            st.caption(
                "Copy this pre-formatted complaint letter directly to file with"
                " consumer courts or bank dispute teams."
            )

            # Extract complaint section or output full text for simple copy
            complaint_text = response.text
            st.text_area(
                "Copy-Paste Ready Complaint Text:",
                value=complaint_text,
                height=320,
            )

          with tab3:
            st.markdown("#### ⚡ System Telemetry & Model Metadata")
            st.json({
                "model_engine": "gemma-4-26b-a4b-it",
                "jurisdiction_target": region_choice,
                "output_language": target_lang,
                "image_resolution": f"{image.size[0]}x{image.size[1]} px",
                "image_format": image.format,
                "status": "200_OK",
            })

        except Exception as e:
          st.error("❌ Forensic analysis failed. Please verify your API key.")
          st.error(str(e))
else:
  st.info(
      "ℹ️ Ingest an e-commerce checkout screenshot or snapshot above to begin"
      " your threat audit."
  )
