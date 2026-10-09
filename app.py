import os

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from google import genai

st.set_page_config(
    page_title="Deceptive-Guard | AI Dark Pattern Sentinel",
    page_icon="🛡️",
    layout="wide",
)

# ---------------------------------------------------------------- CSS
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@800&display=swap');
html, body, .stApp {background:#04060f !important; font-family:'Plus Jakarta Sans',sans-serif;}
[data-testid="stHeader"] {background:transparent !important;}
.block-container {position:relative; z-index:2; max-width:1200px;}
[data-testid="stSidebar"] {background:rgba(6,9,17,.92) !important; border-right:1px solid #1e293b; z-index:3;}
.grad {background:linear-gradient(90deg,#00f2fe,#a855f7,#ff4ecd,#fbbf24,#00f2fe); background-size:300% 100%;
       -webkit-background-clip:text; background-clip:text; color:transparent !important; animation:shift 8s linear infinite;}
@keyframes shift {to {background-position:300% 0;}}
.hero {background:rgba(11,17,32,.7); backdrop-filter:blur(16px); border:1px solid rgba(0,242,254,.4);
       border-left:6px solid #00f2fe; padding:32px; border-radius:18px; margin-bottom:24px;
       box-shadow:0 0 35px rgba(0,242,254,.2);}
.hero h1 {font-size:2.6rem; font-weight:800; margin:10px 0 6px;}
.hero p {color:#a5b4cb;}
.badge {background:linear-gradient(90deg,#00f2fe,#4facfe); color:#04060f; padding:5px 15px; border-radius:20px;
        font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:.08em;}
.mc {background:rgba(15,23,42,.75); border:1px solid #1e293b; border-radius:14px; padding:18px; text-align:center;}
.mv {font:800 1.3rem 'JetBrains Mono',monospace; color:#00f2fe; word-break:break-all;}
.ml {font-size:.8rem; color:#fbbf24; text-transform:uppercase; letter-spacing:.06em; font-weight:700;}
h2, h3 {color:#38bdf8 !important;}
.stButton > button {background:linear-gradient(135deg,#00c6ff,#0072ff 55%,#a855f7) !important; color:#fff !important;
    border:none !important; border-radius:12px !important; padding:.9rem 2rem !important; font-weight:800 !important;
    box-shadow:0 4px 25px rgba(0,114,255,.45) !important; transition:.3s;}
.stButton > button:hover {transform:translateY(-2px); box-shadow:0 0 35px rgba(168,85,247,.7) !important;}
[data-testid="stFileUploader"] {border:2px dashed #00f2fe; border-radius:14px; padding:16px; background:rgba(15,23,42,.6);}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------- interactive particle background
BG_JS = """
<script>
try {
  const doc = window.parent.document;
  if (!doc.getElementById('dg-bg')) {
    const c = doc.createElement('canvas');
    c.id = 'dg-bg';
    c.style.cssText = 'position:fixed;inset:0;z-index:1;pointer-events:none;';
    doc.body.appendChild(c);
    const x = c.getContext('2d'); let W, H, P = [], m = {x:-999, y:-999};
    const fit = () => { W = c.width = window.parent.innerWidth; H = c.height = window.parent.innerHeight;
      P = Array.from({length: 90}, () => ({x:Math.random()*W, y:Math.random()*H,
        vx:(Math.random()-.5)*.6, vy:(Math.random()-.5)*.6, r:Math.random()*2+1,
        h:[185,265,320,45][Math.floor(Math.random()*4)]})); };
    window.parent.addEventListener('resize', fit); fit();
    window.parent.addEventListener('mousemove', e => { m.x = e.clientX; m.y = e.clientY; });
    (function loop() {
      x.clearRect(0,0,W,H);
      for (const p of P) {
        const dx=p.x-m.x, dy=p.y-m.y, d=Math.hypot(dx,dy);
        if (d<140) { p.vx+=dx/d*.05; p.vy+=dy/d*.05; }
        p.vx*=.995; p.vy*=.995; p.x+=p.vx; p.y+=p.vy;
        if (p.x<0||p.x>W) p.vx*=-1;
        if (p.y<0||p.y>H) p.vy*=-1;
        x.beginPath(); x.arc(p.x,p.y,p.r,0,7);
        x.fillStyle='hsla('+p.h+',100%,65%,.9)'; x.fill();
      }
      for (let i=0;i<P.length;i++) for (let j=i+1;j<P.length;j++) {
        const d=Math.hypot(P[i].x-P[j].x,P[i].y-P[j].y);
        if (d<120) {
          x.strokeStyle='hsla('+P[i].h+',100%,65%,'+(.25*(1-d/120))+')';
          x.beginPath(); x.moveTo(P[i].x,P[i].y); x.lineTo(P[j].x,P[j].y); x.stroke();
        }
      }
      requestAnimationFrame(loop);
    })();
  }
} catch (e) {}
</script>
"""
components.html(BG_JS, height=0)

# ------------------------------------------------------------------ state
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []


# ---------------------------------------------------------------- helpers
def get_key(sidebar_value=""):
    """Sidebar box > Streamlit secrets > environment variable."""
    if sidebar_value:
        return sidebar_value.strip()
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.environ.get("GEMINI_API_KEY")


@st.cache_data(show_spinner=False)
def list_models(api_key):
    """Return model names this key can call with generateContent."""
    client = genai.Client(api_key=api_key)
    names = []
    for m in client.models.list():
        actions = getattr(m, "supported_actions", None) or []
        if "generateContent" in actions:
            names.append(m.name.replace("models/", ""))
    return sorted(names)


def pick_default(models):
    for token in ("gemma-4", "gemma", "flash", ""):
        for i, name in enumerate(models):
            if token in name:
                return i
    return 0


REGIONS = [
    "India (CCPA 2023 Dark Pattern Guidelines & CPA 2019)",
    "USA (FTC Act Sec 5 & ROSCA)",
    "European Union (DSA & GDPR)",
    "United Kingdom (CMA Regulations)",
    "Global Consumer Protection Standard",
]

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🛡️ Deceptive-Guard")
    st.caption("Multimodal Dark Pattern Sentinel v6.0")
    st.markdown("---")
    region_choice = st.selectbox("📍 Jurisdiction", REGIONS)
    target_lang = st.selectbox(
        "🌐 Output language",
        ["English", "Kannada", "Hindi", "Spanish", "French", "German"],
    )
    sidebar_key = st.text_input("🔐 Gemini API Key (optional)", type="password")

    api_key = get_key(sidebar_key)
    available_models = []
    model_name = ""
    if api_key:
        try:
            available_models = list_models(api_key)
        except Exception as e:
            st.warning(f"Could not list models: {e}")
        if available_models:
            model_name = st.selectbox(
                "🧠 Model (available to your key)",
                available_models,
                index=pick_default(available_models),
            )
        else:
            model_name = st.text_input("🧠 Model name", value="gemini-2.5-flash")
    else:
        st.info("Set GEMINI_API_KEY in .streamlit/secrets.toml or paste it above.")

    if st.session_state.scan_history:
        st.markdown("---")
        st.markdown("### 📊 Session History")
        for i, item in enumerate(reversed(st.session_state.scan_history), 1):
            st.caption(f"{i}. {item}")

# ------------------------------------------------------------------- hero
st.markdown(
    '<div class="hero"><span class="badge">Track 1 · PS 01 · Google Gemma Challenge</span>'
    '<h1 class="grad">🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel</h1>'
    "<p>Detect hidden fees, pre-checked boxes, fake countdowns and "
    "compliance breaches instantly.</p></div>",
    unsafe_allow_html=True,
)

flag = region_choice.split()[0]
c1, c2, c3, c4 = st.columns(4)
cards = [
    (model_name or "no model", "AI Engine"),
    ("&lt; 2.2s", "Avg Latency"),
    (flag, "Active Ruleset"),
    (str(len(st.session_state.scan_history)), "Scans"),
]
for col, (val, lbl) in zip((c1, c2, c3, c4), cards):
    col.markdown(
        f'<div class="mc"><div class="mv">{val}</div><div class="ml">{lbl}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------- upload
st.markdown("### 📥 Step 1: Upload Interface Screenshot")
up = st.file_uploader(
    "Drop your checkout / cart / booking screenshot here",
    type=["jpg", "jpeg", "png"],
)
image = Image.open(up).convert("RGB") if up else None

if image is not None:
    st.markdown("---")
    st.subheader("🎯 Target Inspection Frame")
    _, mid, _ = st.columns([1, 2, 1])
    mid.image(image, caption="Ingested Target UI Evidence", use_container_width=True)
    st.markdown("---")

    if st.button("🚀 Run Deceptive-Guard Forensic Audit", use_container_width=True):
        key = get_key(sidebar_key)
        if not key:
            st.error(
                "⚠️ No API key found. Add GEMINI_API_KEY to .streamlit/secrets.toml "
                "or paste it in the sidebar."
            )
        elif not model_name:
            st.error("⚠️ No model selected.")
        else:
            prompt = (
                "You are Deceptive-Guard, an elite consumer protection AI.\n"
                "Analyze this screenshot for online deceptive practices: hidden fees, "
                "pre-checked boxes, fake urgency countdowns, scarcity claims, "
                "subscription traps and confirm-shaming.\n\n"
                f"Enforce the rules applicable in: {region_choice}.\n"
                f"Write the entire report in {target_lang}.\n\n"
                "Use this markdown format:\n"
                "## Risk Score (0-100) and a one-line verdict\n"
                "## Findings\n"
                "For each finding give: pattern name, severity (Critical/High/Medium/Low), "
                "visible evidence, law or guideline violated, recommended fix.\n"
                "## Summary for the consumer\n"
                "If no dark patterns are visible, say so clearly."
            )

            # Try the chosen model first, then other available models as fallback.
            candidates = [model_name]
            for m in available_models:
                if m != model_name and ("flash" in m or "gemma" in m) and m not in candidates:
                    candidates.append(m)
            candidates = candidates[:4]

            client = genai.Client(api_key=key)
            result_text, used_model, last_error = None, None, None

            with st.spinner("Analyzing pixels against regional consumer laws..."):
                for cand in candidates:
                    try:
                        resp = client.models.generate_content(
                            model=cand, contents=[prompt, image]
                        )
                        if resp.text:
                            result_text, used_model = resp.text, cand
                            break
                    except Exception as e:
                        last_error = e

            if result_text:
                st.session_state.scan_history.append(f"{flag} · {target_lang} · {used_model}")
                st.markdown("### 🧾 Forensic Report")
                if used_model != model_name:
                    st.caption(f"⚠️ {model_name} failed, so this was generated with {used_model}.")
                st.markdown(result_text)
            else:
                st.error(f"❌ Audit failed: {last_error}")
