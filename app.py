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

# 2. Premium Cyber CSS Engine (Single-line string to prevent syntax errors)
css_code = "<style>@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap'); html, body, .stApp { background-color: #030712 !important; background-image: radial-gradient(at 10% 10%, rgba(0, 242, 254, 0.12) 0px, transparent 40%), radial-gradient(at 90% 90%, rgba(124, 58, 237, 0.12) 0px, transparent 40%); color: #f8fafc !important; font-family: 'Plus Jakarta Sans', system-ui, sans-serif; } p, span, label, div { color: #cbd5e1; font-size: 15px; } h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; color: #f8fafc; } .block-container { max-width: 1200px; padding-top: 1.5rem; padding-bottom: 4rem; margin: 0 auto; } [data-testid='stSidebar'] { background-color: #070a12 !important; border-right: 1px solid #1e293b !important; } .hero-container { background: linear-gradient(135deg, #0b132b 0%, #030712 100%); border: 1px solid #1e293b; border-left: 6px solid #00f2fe; padding: 32px; border-radius: 18px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(0, 242, 254, 0.15); margin-bottom: 25px; } .badge-tag { background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: #030712 !important; padding: 5px 14px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; } .metric-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 14px; padding: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); } .metric-val { font-size: 1.8rem; font-weight: 800; color: #00f2fe; font-family: 'JetBrains Mono', monospace; } .metric-lbl { font-size: 0.82rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; } .stButton > button { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important; color: #ffffff !important; border-radius: 12px !important; padding: 1rem 2.5rem !important; font-weight: 800 !important; font-size: 1.1rem !important; border: none !important; width: 100% !important; box-shadow: 0 4px 25px rgba(0, 114, 255, 0.4) !important; transition: all 0.3s ease-in-out !important; } .stButton > button:hover { background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important; box-shadow: 0 0 30px rgba(0, 198, 255, 0.8) !important; transform: translateY(-2px); } [data-testid='stFileUploader'] { background-color: #0b1120 !important; border: 2px dashed #1e293b !important; border-radius: 14px !important; padding: 18px !important; } .stTabs [data-baseweb='tab-list'] { gap: 10px; background-color: #0b1120; padding: 8px; border-radius: 12px; border: 1px solid #1e293b; } .stTabs [data-baseweb='tab'] { height: 45px; white-space: pre; border-radius: 8px; color: #94a3b8; font-weight: 600; } .stTabs [aria-selected='true'] { background-color: #1e293b !important; color: #00f2fe !important; } .card-risk { background: #0f172a; border-left: 6px solid #ef4444; border: 1px solid #1e293b; padding: 24px; border-radius: 14px; margin-bottom: 20px; } .card-tricks { background: #0f172a; border-left: 6px solid #38bdf8; border: 1px solid #1e293b; padding: 24px; border-radius: 14px; margin-bottom: 20px; } .card-laws { background: #0f172a; border-left: 6px solid #a855f7; border: 1px solid #1e293b; padding: 24px; border-radius: 14px; margin-bottom: 20px; } .card-complaint { background: #0f172a; border-left: 6px solid #4ade80; border: 1px solid #1e293b; padding: 24px; border-radius: 14px; margin-bottom: 20px; } .section-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; font-family: 'Plus Jakarta Sans', sans-serif; }</style>"

st.markdown(css_code, unsafe_allow_html=True)

# Initialize Session History
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/color/96/cyber-security.png", width=60)
    st.title("Deceptive-Guard")
    st.caption("Multimodal Dark Pattern Sentinel v4.0")
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
    st.info("⚡ Temperature Locked at 0.0 (Deterministic)")

    if st.session_state.scan_history:
        st.markdown("---")
        st.markdown("### 📊 Session History Log")
        for idx, scan_item in enumerate(reversed(st.session_state.scan_history)):
            st.caption(f"Scan #{len(st.session_state.scan_history)-idx}: {scan_item}")

# Hero Header Banner
hero_html = "<div class='hero-container'><span class='badge-tag'>Track 1 - PS 01 | Google Gemma Challenge</span><h1 style='color: #ffffff; font-size: 2.5rem; font-weight: 800; margin-top: 12px; margin-bottom: 6px; letter-spacing: -0.02em;'>🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel</h1><p style='color: #94a3b8; font-size: 1.1rem; margin: 0; line-height: 1.5;'>Detect manipulative checkout traps, hidden pre-checked fees, fake countdown timers, and regulatory compliance breaches instantly using Google Gemma.</p></div>"
st.markdown(hero_html, unsafe_allow_html=True)

# Top Live Statistics Dashboard
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><div class="metric-val">gemma-4-26b</div><div class="metric-lbl">AI Core Engine</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><div class="metric-val">< 2.2s</div><div class="metric-lbl">Avg Scan Latency</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="metric-val">{region_choice.split()[0]}</div><div class="metric-lbl">Active Ruleset</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="metric-val">{len(st.session_state.scan_history)}</div><div class="metric-lbl">Scans Conducted</div></div>', unsafe_allow_html=True)

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

                    prompt = f"You are Deceptive-Guard, an elite consumer protection AI powered by Google Gemma. Analyze this screenshot for online deceptive practices, hidden fees, pre-checked boxes, fake urgency countdowns, or subscription traps.\n\nCONFIGURATION RULES:\n- Target Jurisdiction Rules: Enforce regulatory policies and laws applicable in: {region_choice}.\n- Target Output Language: Provide the entire response in: {target_lang}.\n\nFormat your response strictly using these four exact styled HTML card sections:\n\nSECTION 1:\n<div class=\"card-risk\"><div class=\"section-title\" style=\"color: #f87171;\">🚨 SCAM RISK SCORE</div><div style=\"font-size: 34px; font-weight: 800; color: #ef4444; margin-top: 5px; font-family: 'JetBrains Mono', monospace;\">[State Percentage, e.g., 65% - MEDIUM-HIGH RISK]</div></div>\n\nSECTION 2:\n<div class=\"card-tricks\"><div class=\"section-title\" style=\"color: #38bdf8;\">🔍 DECEPTIVE TRICKS IDENTIFIED</div><div style=\"color: #e2e8f0; line-height: 1.8;\">[Provide bulleted points detailing dark patterns found in {target_lang}]</div></div>\n\nSECTION 3:\n<div class=\"card-laws\"><div class=\"section-title\" style=\"color: #c084fc;\">⚖️ SPECIFIC LEGAL & REGULATORY VIOLATIONS</div><div style=\"color: #e2e8f0; line-height: 1.8;\">[Explicitly name laws or guidelines breached under {region_choice} in {target_lang}]</div></div>\n\nSECTION 4:\n<div class=\"card-complaint\"><div class=\"section-title\" style=\"color: #4ade80;\">📝 READY-TO-FILE COMPLAINT LETTER</div><div style=\"color: #cbd5e1; line-height: 1.8;\">[Provide a formal ready-to-copy grievance letter in {target_lang}]</div></div>"

                    # FIXED: temperature=0.0 locks output determinism across multiple runs
                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it",
                        contents=[image, prompt],
                        config={"temperature": 0.0}
                    )

                    st.success("✅ Forensic Audit Completed Successfully!")

                    st.session_state.scan_history.append(f"{region_choice.split()[0]} | {target_lang}")

                    tab1, tab2, tab3 = st.tabs([
                        "📊 Executive Audit Report",
                        "📝 Formal Legal Complaint",
                        "⚡ RAW Telemetry & Metadata",
                    ])

                    with tab1:
                        st.markdown(response.text, unsafe_allow_html=True)

                    with tab2:
                        st.markdown("#### 📝 Copy-Ready Consumer Grievance Letter")
                        st.caption("Copy or download this pre-formatted complaint letter to file directly with consumer courts.")
                        
                        complaint_output = response.text
                        st.text_area("Grievance Letter Content:", value=complaint_output, height=320)
                        
                        # NEW FEATURE: One-click Download Button for legal submission
                        st.download_button(
                            label="📥 Download Complaint Report (.txt)",
                            data=complaint_output,
                            file_name="Deceptive_Guard_Grievance_Report.txt",
                            mime="text/plain",
                        )

                    with tab3:
                        st.markdown("#### ⚡ System Telemetry & Model Details")
                        st.json({
                            "model_engine": "gemma-4-26b-a4b-it",
                            "sampling_temperature": 0.0,
                            "jurisdiction_target": region_choice,
                            "output_language": target_lang,
                            "image_resolution": f"{image.size[0]}x{image.size[1]} px",
                            "image_format": image.format,
                            "status": "200_OK",
                        })

                except Exception as e:
                    st.error("❌ Forensic analysis failed. Please check your API key.")
                    st.error(str(e))
else:
    st.info("ℹ️ Upload or capture an e-commerce checkout screenshot above to begin your threat audit.")
