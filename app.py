from google import genai
from PIL import Image
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Deceptive-Guard | Enterprise Scam Scanner",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Winning UI Cyber-Security Theme & Glowing Accents
st.markdown(
    """
    <style>
    .stApp {
        background-color: #07090e;
        color: #f3f4f6;
    }
    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        margin: 0 auto;
    }
    /* Winning UI Header Card */
    .hero-box {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #374151;
        border-left: 5px solid #3b82f6;
        padding: 30px;
        border-radius: 14px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }
    .badge {
        background-color: #1e3a8a;
        color: #93c5fd;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.6);
    }
    .report-card {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 35px;
        border-radius: 14px;
        margin-top: 20px;
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.4);
    }
    .report-card p, .report-card li {
        color: #e5e7eb !important;
        font-size: 16px;
        line-height: 1.8;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar with hidden API settings
with st.sidebar:
  st.image("https://img.icons8.com/color/96/cyber-security.png", width=65)
  st.title("Deceptive-Guard")
  st.caption("Enterprise Consumer Protection")
  st.markdown("---")
  with st.expander("🔐 API Settings"):
    sidebar_key = st.text_input("Gemini API Key", type="password")
  st.markdown("---")
  st.success("🟢 Gemma Engine Online")
  st.info("⚡ Multimodal Vision Active")

# Winning UI Hero Banner
st.markdown(
    """
    <div class="hero-box">
        <span class="badge">Track 1 - PS 01 | Google Gemma Challenge</span>
        <h1 style="color: #ffffff; font-size: 2.4rem; margin-top: 12px; margin-bottom: 8px;">🛡️ Deceptive-Guard: UI Trap Scanner</h1>
        <p style="color: #9ca3af; font-size: 1.15rem; margin: 0;">Detect hidden checkout traps, deceptive dark patterns, and regulatory policy violations instantly using Gemma AI.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Intake Section
st.markdown("### 📥 Step 1: Upload Targeted UI Evidence")
input_method = st.radio(
    "Choose input type:",
    ["📁 Upload Image File", "📸 Take Live Photo"],
    horizontal=True,
    label_visibility="collapsed",
)

image = None
if "Upload" in input_method:
  uploaded_file = st.file_uploader(
      "Drop your checkout or shopping cart screenshot...",
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
  st.subheader("🎯 Target Evidence Stream")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.image(image, use_container_width=True)

  st.markdown("---")
  if st.button(
      "🚀 Run Deceptive-Guard Forensic Scan Now", use_container_width=True
  ):
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
          "Running multi-vector forensic scan through Gemma multimodal"
          " layers..."
      ):
        try:
          client = genai.Client(api_key=active_key)

          # Prompt explicitly forcing policy violations and simple language
          prompt = """
                    You are an expert consumer protection AI powered by Gemma. Analyze this shopping or checkout screenshot for online tricks, hidden fees, fake urgent timers, or sneaky pre-checked boxes.
                    
                    Use clear, simple everyday language that normal people can easily understand, avoiding heavy legal jargon.
                    
                    Format your response strictly using these exact sections:
                    1. <h3 style="color: #ff4d4d; margin-top: 0;">🚨 Scam Risk Score</h3><div style="font-size: 38px; font-weight: 800; color: #ff4d4d; margin: 10px 0;">[State percentage, e.g., 90% - HIGH RISK CRITICAL]</div>
                    2. <h3 style="color: #38bdf8; margin-top: 25px;">🔍 What Tricks Were Found</h3> [Explain in simple words what deceptive tricks the website is pulling]
                    3. <h3 style="color: #fbbf24; margin-top: 25px;">⚖️ Policies & Laws Being Violated</h3> [Explicitly name and explain what consumer protection laws, FTC unfair trade rules, or e-commerce regulations this breaks in simple words]
                    4. <h3 style="color: #34d399; margin-top: 25px;">📝 Simple Complaint Letter</h3> [Provide an easy ready-to-use copy-paste text report a consumer can file against them]
                    """

          response = client.models.generate_content(
              model="gemma-4-26b-a4b-it", contents=[image, prompt]
          )

          st.success("✅ Forensic Audit Completed Successfully!")
          st.markdown(
              f'<div class="report-card">{response.text}</div>',
              unsafe_allow_html=True,
          )

        except Exception as e:
          st.error("❌ Connection error. Please check your API key.")
          st.error(str(e))
else:
  st.info("ℹ️ Upload an interface screenshot above to begin your security scan.")