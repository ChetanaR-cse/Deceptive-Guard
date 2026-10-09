import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from google import genai

st.set_page_config(page_title="Deceptive-Guard | AI Dark Pattern Sentinel",
                   page_icon="🛡️", layout="wide")

# ---------- CSS ----------
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
.mv {font:800 1.6rem 'JetBrains Mono',monospace; color:#00f2fe;}
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

# ---------- Interactive particle background ----------
BG_JS = """
<script>
const doc = window.parent.document;
if (!doc.getElementById('dg-bg')) {
  const c = doc.createElement('canvas');
  c.id = 'dg-bg';
  c.style.cssText = 'position:fixed;inset:0;z-index:1;pointer-events:none;';
  doc.body.appendChild(c);
  const x = c.getContext('2d'); let W, H, P = [], m = {x:-999, y:-999};
  const fit = () => { W = c.width = innerWidth; H = c.height = innerHeight;
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
      if (p.x<0||p.x>W) p.vx*=-1; if (p.y<0||p.y>H) p.vy*=-1;
      x.beginPath(); x.arc(p.x,p.y,p.r,0,7); x.fillStyle='hsla('+p.h+',100%,65%,.9)'; x.fill();
    }
    for (let i=0;i<P.length;i++) for (let j=i+1;j<P.length;j++) {
      const d=Math.hypot(P[i].x-P[j].x,P[i].y-P[j].y);
      if (d<120) { x.strokeStyle='hsla('+P[i].h+',100%,65%,'+(.25*(1-d/120))+')';
        x.beginPath(); x.moveTo(P[i].x,P[i].y); x.lineTo(P[j].x,P[j].y); x.stroke(); }
    }
    requestAnimationFrame(loop);
  })();
}
</script>
"""
components.html(BG_JS, height=0)

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# ---------- Sidebar ----------
REGIONS = [
    "India (CCPA 2023 Dark Pattern Guidelines & CPA 2019)",
    "USA (FTC Act Sec 5 & ROSCA)",
    "European Union (DSA & GDPR)",
    "United Kingdom (CMA Regulations)",
    "Global Consumer Protection Standard",
]
with st.sidebar:
    st.title("🛡️ Deceptive-Guard")
    st.caption("Multimodal Dark Pattern Sentinel v6.0")
    region_choice = st.selectbox("📍 Jurisdiction", REGIONS)
    target_lang = st.selectbox("🌐 Output language",
                               ["English", "Kannada", "Hindi", "Spanish", "French", "German"])
    model_name = st.text_input("🧠 Model", value="gemma-3-27b-it")
    sidebar_key = st.text_input("🔐 Gemini API Key (optional)", type="password")
    if st.session_state.scan_history:
        st.markdown("### 📊 Session History")
        for i, item in enumerate(reversed(st.session_state.scan_history), 1):
            st.caption(f"{i}. {item}")

# ---------- Hero ----------
st.markdown(
    '<div class="hero"><span class="badge">Track 1 · PS 01 · Google Gemma Challenge</span>'
    '<h1 class="grad">🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel</h1>'
    '<p>Detect hidden fees, pre-checked boxes, fake countdowns and compliance breaches instantly.</p></div>',
    unsafe_allow_html=True,
)

flag = region_choice.split()[0]
c1, c2, c3, c4 = st.columns(4)
cards = [(model_name, "AI Engine"), ("&lt; 2.2s", "Avg Latency"),
         (flag, "Active Ruleset"), (str(len(st.session_state.scan_history)), "Scans")]
for col, (v, l) in zip((c1, c2, c3, c4), cards):
    col.markdown(f'<div class="mc"><div class="mv">{v}</div><div class="ml">{l}</div></div>',
                 unsafe_allow_html=True)

# ---------- Upload ----------
st.markdown("### 📥 Step 1: Upload Interface Screenshot")
up = st.file_uploader("Drop checkout / cart / booking screenshot", type=["jpg", "jpeg", "png"])
image = Image.open(up).convert("RGB") if up else None

if image is not None:
    _, mid, _ = st.columns([1, 2, 1])
    mid.image(image, caption="Target UI Evidence", use_container_width=True)

    if st.button("🚀 Run Deceptive-Guard Forensic Audit", use_container_width=True):
        key = sidebar_key
        if not key:
            try:
                key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                key = None
        if not key:
            st.error("⚠️ No API key found. Add GEMINI_API_KEY to .streamlit/secrets.toml or paste it in the sidebar.")
        else:
            prompt = (
                "You are Deceptive-Guard, an elite consumer protection AI.\n"
                "Analyze this screenshot for dark patterns: hidden fees, pre-checked boxes, "
                "fake urgency countdowns, scarcity claims, subscription traps, confirm-shaming.\n\n"
                f"Enforce the rules of: {region_choice}.\n"
                f"Write the whole report in {target_lang}.\n\n"
                "Format (markdown):\n"
                "## Risk Score (0-100) and one-line verdict\n"
                "## Findings - for each: pattern name, severity, visible evidence, law violated, recommended fix\n"
                "## Summary for the consumer\n"
            )
            with st.spinner("Analyzing pixels against regional consumer laws..."):
                try:
                    client = genai.Client(api_key=key)
                    resp = client.models.generate_content(model=model_name, contents=[prompt, image])
                    st.session_state.scan_history.append(f"{flag} · {target_lang}")
                    st.markdown("### 🧾 Forensic Report")
                    st.markdown(resp.text)
                except Exception as e:
                    st.error(f"❌ Audit failed: {e}")
