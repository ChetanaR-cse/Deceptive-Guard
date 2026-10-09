from google import genai
from PIL import Image
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Deceptive-Guard | Enterprise Scam Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CYBERSECURITY THEME
# =========================================================
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

    .stButton > button {
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

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.6);
    }

    .report-card {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 25px;
        border-radius: 14px;
        margin-top: 20px;
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.4);
        color: #e5e7eb;
    }

    .report-card h3 {
        color: #60a5fa;
        margin-top: 1.5rem;
    }

    .report-card p,
    .report-card li {
        color: #e5e7eb;
        font-size: 16px;
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/cyber-security.png",
        width=65,
    )
    st.title("Deceptive-Guard")
    st.caption("Enterprise Consumer Protection")
    st.markdown("---")

    with st.expander("🔐 API Settings"):
        sidebar_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Your key is used to authenticate requests to the Google GenAI API.",
        )

    st.markdown("---")
    st.success("🟢 Gemma Engine Ready")
    st.info("⚡ Multimodal Vision Enabled")

# =========================================================
# HERO BANNER
# =========================================================
st.markdown(
    """
    <div class="hero-box">
        <span class="badge">
            Track 1 - PS 01 | Google Gemma Challenge
        </span>
        <h1 style="
            color: #ffffff;
            font-size: 2.4rem;
            margin-top: 12px;
            margin-bottom: 8px;
        ">
            🛡️ Deceptive-Guard: UI Trap Scanner
        </h1>
        <p style="
            color: #9ca3af;
            font-size: 1.15rem;
            margin: 0;
        ">
            Detect hidden checkout traps, deceptive dark patterns,
            suspicious fees, and potentially misleading interface
            practices using multimodal AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# IMAGE INPUT
# =========================================================
st.markdown("### 📥 Step 1: Upload Targeted UI Evidence")

input_method = st.radio(
    "Choose input type:",
    ["📁 Upload Image File", "📸 Take Live Photo"],
    horizontal=True,
    label_visibility="collapsed",
)

image = None

if input_method == "📁 Upload Image File":
    uploaded_file = st.file_uploader(
        "Upload a checkout, shopping cart, or website screenshot",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception:
            st.error("Could not read this image. Please upload a valid image.")
else:
    camera_image = st.camera_input("Capture screenshot evidence")

    if camera_image is not None:
        try:
            image = Image.open(camera_image).convert("RGB")
        except Exception:
            st.error("Could not read the captured image.")

# =========================================================
# DISPLAY EVIDENCE
# =========================================================
if image is not None:
    st.markdown("---")
    st.subheader("🎯 Target Evidence")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            image,
            caption="Image selected for analysis",
            use_container_width=True,
        )

    st.markdown("---")

    # =====================================================
    # SCAN BUTTON
    # =====================================================
    if st.button(
        "🚀 Run Deceptive-Guard Forensic Scan",
        use_container_width=True,
    ):
        active_key = sidebar_key.strip()

        # Fall back to Streamlit secrets if configured.
        if not active_key:
            try:
                active_key = st.secrets["GEMINI_API_KEY"]
            except (KeyError, FileNotFoundError):
                active_key = ""

        if not active_key:
            st.error(
                "Authentication error: Enter your API key in the sidebar "
                "or configure GEMINI_API_KEY in Streamlit secrets."
            )

        else:
            prompt = """
You are Deceptive-Guard, an AI assistant that helps consumers
identify potentially deceptive shopping and checkout interfaces.

Analyze the supplied screenshot carefully. Look for visible evidence
of hidden fees, misleading discounts, fake urgency, countdown timers,
preselected add-ons, difficult cancellation, confusing consent,
misleading buttons, or other possible dark patterns.

Use clear, simple language. Do not invent details that are not visible.

Return your response in Markdown using exactly these sections:

### 🚨 Scam Risk Score
Give an AI-estimated scam/deception risk percentage from 0% to 100%
and a risk level: LOW, MEDIUM, HIGH, or CRITICAL.
Explain briefly that this is an estimate, not a statistically validated
probability or proof of illegal activity.

### 🔍 What Tricks Were Found
List each visible suspicious pattern.
Explain the evidence in the screenshot.
If no clear evidence is visible, say so.
Distinguish confirmed observations from uncertain suspicions.

### ⚖️ Policies & Laws Potentially Involved
Identify potentially relevant consumer-protection rules or laws only
when applicable to the visible facts.
If the jurisdiction is unknown, state that the applicable law depends
on the user's location.
Never claim that a law was definitely violated without sufficient
evidence. Explain that legal conclusions require verification.

### 📝 Complaint Letter Draft
Write a copy-ready complaint draft with placeholders for:
- Consumer name and contact details
- Company or website name
- Date and description of the incident
- Amount charged, if applicable
- Evidence attached
- Requested resolution

Do not invent company names, dates, charges, or personal details.
Clearly mark placeholders that the consumer must complete.

### ✅ Recommended Next Steps
Give practical safety steps based on the screenshot.
Suggest saving evidence and checking official reporting channels
when appropriate.

FORMATTING RULES:
- Use proper Markdown headings and bullet points.
- Use **bold text** for important labels and findings.
- Every opening bold marker must have a matching closing marker.
- Do not display Markdown symbols literally.
- Do not put the entire response inside a code block.
- Do not invent evidence, statistics, legal citations, or findings.
"""

            with st.spinner(
                "Analyzing screenshot with the Gemma multimodal model..."
            ):
                try:
                    client = genai.Client(api_key=active_key)

                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it",
                        contents=[image, prompt],
                    )

                    report = response.text

                    if not report or not report.strip():
                        st.error(
                            "The AI returned an empty report. Please try again."
                        )
                    else:
                        st.success("✅ Screenshot analysis completed!")

                        # Render Markdown INSIDE the report container.
                        # This correctly formats **bold**, headings and lists.
                        with st.container(border=True):
                            st.markdown(
                                '<div class="report-card">',
                                unsafe_allow_html=True,
                            )

                            st.markdown(report)

                            st.markdown(
                                "</div>",
                                unsafe_allow_html=True,
                            )

                        st.caption(
                            "AI-generated assessment only. Verify findings "
                            "and applicable laws before taking action."
                        )

                        # Optional copy-ready plain text version.
                        st.download_button(
                            label="📥 Download Report",
                            data=report,
                            file_name="deceptive_guard_report.md",
                            mime="text/markdown",
                        )

                except Exception as e:
                    st.error(
                        "The scan failed. Check your internet connection, "
                        "API key, model availability, and API permissions."
                    )
                    st.exception(e)

else:
    st.info(
        "Upload an interface screenshot or take a photo above "
        "to begin your security scan."
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "Deceptive-Guard | AI-assisted consumer protection. "
    "Results are informational and do not constitute legal advice."
)
