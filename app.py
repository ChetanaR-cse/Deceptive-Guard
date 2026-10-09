import html
import json
import os

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Deceptive-Guard | AI Dark Pattern Sentinel",
    page_icon="🛡️",
    layout="wide",
)

# ================================================================== STYLE
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@700;800&display=swap');
html, body, .stApp {background:#04060f !important; font-family:'Plus Jakarta Sans',sans-serif; color:#e2e8f0;}
.stApp .stMarkdown p, .stApp .stMarkdown li, .stApp label p {font-family:'Plus Jakarta Sans',sans-serif;}
.stApp .stMarkdown p, .stApp label p {color:#cbd5e1; font-size:16px;}
/* keep Streamlit's icon font intact so icons never render as words like "add" or "upload" */
.stApp [data-testid="stIconMaterial"], .stApp .material-symbols-rounded, .stApp span[class*="material"] {
    font-family:'Material Symbols Rounded','Material Symbols Outlined' !important; font-size:1.4rem !important;}
[data-testid="stFileUploaderDropzone"] {display:flex; align-items:center; gap:14px; flex-wrap:wrap;}
[data-testid="stFileUploaderDropzone"] button {white-space:nowrap;}
[data-testid="stFileUploaderDropzoneInstructions"] {line-height:1.4 !important;}
[data-testid="stFileUploaderDropzoneInstructions"] span, [data-testid="stFileUploaderDropzoneInstructions"] small {display:block; line-height:1.4 !important;}
[data-testid="stFileUploaderFile"] {align-items:center;}
[data-testid="stFileUploaderFileName"] {overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
[data-testid="stHeader"] {background:transparent !important;}
.block-container {position:relative; z-index:2; max-width:1200px; padding-top:1.5rem;}
[data-testid="stSidebar"] {background:rgba(6,9,17,.94) !important; border-right:1px solid #1e293b; z-index:3;}

.grad {background:linear-gradient(90deg,#00f2fe,#a855f7,#ff4ecd,#fbbf24,#00f2fe); background-size:300% 100%;
       -webkit-background-clip:text; background-clip:text; color:transparent !important; animation:shift 8s linear infinite;}
@keyframes shift {to {background-position:300% 0;}}

.hero {background:rgba(11,17,32,.72); backdrop-filter:blur(16px); border:1px solid rgba(0,242,254,.4);
       border-left:6px solid #00f2fe; padding:30px 34px; border-radius:18px; margin-bottom:24px;
       box-shadow:0 0 35px rgba(0,242,254,.18);}
.hero-title {font-size:2.5rem; font-weight:800; line-height:1.15; margin:12px 0 8px; letter-spacing:-.02em;}
.hero-sub {color:#a5b4cb; font-size:1.1rem; line-height:1.6;}
.badge {background:linear-gradient(90deg,#00f2fe,#4facfe); color:#04060f; padding:5px 15px; border-radius:20px;
        font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:.08em;}

.mc {background:rgba(15,23,42,.8); border:1px solid #1e293b; border-radius:14px; padding:18px; text-align:center;}
.mv {font:800 1.25rem 'JetBrains Mono',monospace; color:#00f2fe; word-break:break-all;}
.ml {font-size:.78rem; color:#fbbf24; text-transform:uppercase; letter-spacing:.08em; font-weight:700; margin-top:4px;}

.sec {font-size:1.5rem; font-weight:800; margin:26px 0 12px; letter-spacing:-.01em;}
.c-cyan {color:#22d3ee;} .c-pink {color:#ff6ec7;} .c-amber {color:#fbbf24;} .c-green {color:#34d399;} .c-violet {color:#c084fc;}

.stButton > button, .stDownloadButton > button {background:linear-gradient(135deg,#00c6ff,#0072ff 55%,#a855f7) !important;
    color:#fff !important; border:none !important; border-radius:12px !important; padding:.9rem 2rem !important;
    font-weight:800 !important; font-size:1.05rem !important; box-shadow:0 4px 25px rgba(0,114,255,.45) !important; transition:.3s;}
.stButton > button:hover, .stDownloadButton > button:hover {transform:translateY(-2px); box-shadow:0 0 35px rgba(168,85,247,.7) !important;}
[data-testid="stFileUploader"] {border:2px dashed #00f2fe; border-radius:14px; padding:16px; background:rgba(15,23,42,.6);}

.stTabs [data-baseweb="tab-list"] {gap:8px; background:rgba(11,17,32,.9); padding:8px; border-radius:12px; border:1px solid #1e293b;}
.stTabs [data-baseweb="tab"] {height:46px; border-radius:8px; color:#94a3b8; font-weight:700; font-size:15px;}
.stTabs [aria-selected="true"] {background:#1e293b !important; color:#22d3ee !important;}
textarea {font-family:'JetBrains Mono',monospace !important; font-size:14px !important; line-height:1.6 !important;
          background:#0b1120 !important; color:#e2e8f0 !important;}

.score-wrap {display:flex; gap:30px; align-items:center; background:rgba(15,23,42,.8); border:1px solid #1e293b;
             border-radius:18px; padding:26px; flex-wrap:wrap;}
.ring {width:150px; height:150px; border-radius:50%; flex-shrink:0; display:grid; place-items:center;
       background:conic-gradient(var(--c) calc(var(--p)*1%), rgba(148,163,184,.18) 0); box-shadow:0 0 40px var(--c);}
.ringin {width:116px; height:116px; border-radius:50%; background:#070b18; display:grid; place-items:center;
         font:800 2.4rem 'JetBrains Mono',monospace; color:var(--c);}
.lvl {display:inline-block; font:800 .8rem 'JetBrains Mono',monospace; letter-spacing:.1em; padding:4px 14px;
      border-radius:99px; background:var(--c); color:#04060f; margin-bottom:8px;}
.verdict {font-size:1.45rem; font-weight:800; color:#f8fafc; line-height:1.35; margin-bottom:8px;}
.summary {color:#b6c2d6; font-size:1.02rem; line-height:1.7;}

.fcard {background:rgba(15,23,42,.8); border:1px solid #1e293b; border-left:6px solid var(--c); border-radius:16px;
        padding:22px 24px; margin-bottom:18px;}
.fhead {display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:12px;}
.ftitle {font-size:1.25rem; font-weight:800; color:var(--c);}
.sev {font:800 .72rem 'JetBrains Mono',monospace; letter-spacing:.08em; padding:4px 12px; border-radius:99px;
      background:var(--c); color:#04060f;}
.flabel {font-size:.78rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; margin:14px 0 4px;}
.ftext {color:#d5deec; font-size:1rem; line-height:1.7;}

.lcard {background:rgba(15,23,42,.8); border:1px solid #1e293b; border-top:4px solid #c084fc; border-radius:14px;
        padding:18px 22px; margin-bottom:14px;}
.lname {font-size:1.1rem; font-weight:800; color:#c084fc;}
.lsec {font:700 .85rem 'JetBrains Mono',monospace; color:#fbbf24; margin:2px 0 8px;}

.tip {background:rgba(52,211,153,.08); border:1px solid rgba(52,211,153,.35); border-radius:12px; padding:12px 16px;
      margin-bottom:10px; color:#d1fae5; font-size:1rem; line-height:1.6;}
.portal {background:rgba(15,23,42,.8); border:1px solid #1e293b; border-left:5px solid #22d3ee; border-radius:12px;
         padding:14px 18px; margin-bottom:10px;}
.pname {font-weight:800; color:#22d3ee; font-size:1.05rem;}
.pdesc {color:#b6c2d6; font-size:.95rem; margin-top:2px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ===================================================== PARTICLE BACKGROUND
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

# ======================================================================= STATE
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "report" not in st.session_state:
    st.session_state.report = None

# ===================================================================== HELPERS
def H(markup):
    """Flatten HTML so Streamlit's markdown never treats indented lines as code."""
    return "".join(line.strip() for line in markup.splitlines())


def esc(value):
    return html.escape(str(value if value is not None else ""))


def get_key(sidebar_value=""):
    if sidebar_value:
        return sidebar_value.strip()
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.environ.get("GEMINI_API_KEY")


@st.cache_data(show_spinner=False)
def list_models(api_key):
    client = genai.Client(api_key=api_key)
    names = []
    for m in client.models.list():
        actions = getattr(m, "supported_actions", None) or []
        if "generateContent" in actions:
            names.append(m.name.replace("models/", ""))
    return sorted(names)


def pick_default(models):
    for token in ("gemma", "flash", ""):
        for i, name in enumerate(models):
            if token in name:
                return i
    return 0


def parse_json(text):
    if not text:
        return None
    cleaned = text.strip()
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(cleaned[start:end + 1])
    except Exception:
        return None


def generate(client, model, prompt, image):
    """Try JSON mode first; fall back to a plain request if the model rejects it."""
    try:
        cfg = types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2)
        return client.models.generate_content(model=model, contents=[prompt, image], config=cfg)
    except Exception:
        return client.models.generate_content(model=model, contents=[prompt, image])


REGIONS = [
    "India (CCPA 2023 Dark Pattern Guidelines & CPA 2019)",
    "USA (FTC Act Sec 5 & ROSCA)",
    "European Union (DSA & GDPR)",
    "United Kingdom (CMA Regulations)",
    "Global Consumer Protection Standard",
]

FILING = {
    "India": [
        ("National Consumer Helpline (NCH)", "Call 1915 or file online at consumerhelpline.gov.in. Fastest first step."),
        ("CCPA complaint", "Email or file via the Central Consumer Protection Authority route linked on consumerhelpline.gov.in."),
        ("e-Daakhil", "File a formal case before a Consumer Commission at edaakhil.nic.in."),
    ],
    "USA": [
        ("FTC - ReportFraud", "reportfraud.ftc.gov. Report deceptive or unfair online practices."),
        ("State Attorney General", "File with your state consumer protection office."),
        ("CFPB (if payment related)", "consumerfinance.gov/complaint"),
    ],
    "European": [
        ("European Consumer Centres Network", "ec.europa.eu/consumers/odr and your national ECC office."),
        ("National consumer authority", "Report to the consumer protection authority of the trader's or your country."),
        ("Data protection authority", "If personal data was misused, contact your national DPA."),
    ],
    "United": [
        ("Citizens Advice consumer service", "Call 0808 223 1133 or use citizensadvice.org.uk."),
        ("CMA", "Report systemic issues through the Competition and Markets Authority."),
        ("Trading Standards", "Your local council Trading Standards office."),
    ],
    "Global": [
        ("econsumer.gov", "International portal for cross-border online consumer complaints."),
        ("Your national consumer authority", "File with the consumer body in your country of residence."),
        ("Payment provider / card issuer", "Ask for a chargeback if you were charged deceptively."),
    ],
}

SEV_COLOR = {"critical": "#fb7185", "high": "#fb923c", "medium": "#fbbf24", "low": "#34d399"}


def risk_style(score):
    if score >= 75:
        return "#fb7185", "CRITICAL RISK"
    if score >= 50:
        return "#fb923c", "HIGH RISK"
    if score >= 25:
        return "#fbbf24", "MODERATE RISK"
    return "#34d399", "LOW RISK"


def build_prompt(region, lang):
    return (
        "You are Deceptive-Guard, an expert consumer-protection and dark-pattern forensic analyst.\n"
        "Carefully read EVERY element of this screenshot (text, prices, checkboxes, buttons, timers, banners, "
        "colours, default selections, small print). Identify dark patterns such as hidden or drip pricing, "
        "pre-checked add-ons, fake urgency or countdowns, false scarcity, subscription traps, confirm-shaming, "
        "misdirection, forced continuity, bait-and-switch, disguised ads, and misleading obligations.\n"
        "Only report what is genuinely visible. Quote the exact on-screen text as evidence.\n\n"
        f"Jurisdiction to apply: {region}.\n"
        f"Write every text value in {lang}.\n\n"
        "Respond with ONLY valid JSON, no markdown fences, in exactly this shape:\n"
        "{\n"
        '  "risk_score": 0-100 integer,\n'
        '  "verdict": "one punchy headline sentence",\n'
        '  "summary": "2-3 sentence plain-language summary for the consumer",\n'
        '  "service_name": "website/app/brand visible, or Unknown",\n'
        '  "findings": [\n'
        "    {\n"
        '      "pattern": "name of the dark pattern",\n'
        '      "severity": "critical|high|medium|low",\n'
        '      "evidence": "exact visible text/UI element and where it appears",\n'
        '      "why_tricky": "how it tricks the user, step by step",\n'
        '      "psychology": "the cognitive bias exploited (e.g. loss aversion, anchoring, default effect)",\n'
        '      "laws": [{"law": "name of law/guideline", "section": "clause/section/annex number if known", '
        '"how_violated": "one sentence"}],\n'
        '      "fix": "how the business should correct it"\n'
        "    }\n"
        "  ],\n"
        '  "consumer_advice": ["3-5 short practical actions the user should take now"],\n'
        '  "complaint": {\n'
        '    "subject": "email subject line",\n'
        '    "body": "a complete formal complaint letter addressed to the relevant authority, ready to file. '
        "Include: date placeholder, complainant placeholders [Your Name] [Address] [Phone] [Email], "
        "service name, order/transaction placeholder [Order ID], clear numbered description of each violation "
        "with the on-screen evidence, the specific laws and sections breached, the relief sought "
        '(refund, removal of the practice, penalty review), and a polite closing. Use \\n for line breaks."\n'
        "  }\n"
        "}\n"
        "If no dark patterns are visible, return a low score, an empty findings list and a short complaint note "
        "saying no complaint is needed."
    )


# ================================================================== RENDERING
def section_findings(d):
    findings = d.get("findings") or []
    st.markdown('<div class="sec c-pink">🔍 Dark pattern findings</div>', unsafe_allow_html=True)
    if not findings:
        st.success("✅ No dark patterns detected in this screenshot.")
    for f in findings:
        sev = str(f.get("severity", "medium")).lower()
        c = SEV_COLOR.get(sev, "#38bdf8")
        st.markdown(H(f"""
            <div class="fcard" style="--c:{c}">
              <div class="fhead"><div class="ftitle">{esc(f.get("pattern"))}</div><div class="sev">{esc(sev.upper())}</div></div>
              <div class="flabel c-cyan">👁️ Visible evidence</div><div class="ftext">{esc(f.get("evidence"))}</div>
              <div class="flabel c-pink">🎭 Why it is tricky</div><div class="ftext">{esc(f.get("why_tricky"))}</div>
              <div class="flabel c-violet">🧠 Psychology exploited</div><div class="ftext">{esc(f.get("psychology"))}</div>
              <div class="flabel c-green">🛠️ How the business should fix it</div><div class="ftext">{esc(f.get("fix"))}</div>
            </div>"""), unsafe_allow_html=True)

    advice = d.get("consumer_advice") or []
    if advice:
        st.markdown('<div class="sec c-green">✅ What you should do now</div>', unsafe_allow_html=True)
        for a in advice:
            st.markdown(f'<div class="tip">{esc(a)}</div>', unsafe_allow_html=True)


def section_laws(d):
    st.markdown('<div class="sec c-violet">⚖️ Laws and guidelines violated</div>', unsafe_allow_html=True)
    any_law = False
    for f in d.get("findings") or []:
        for law in f.get("laws") or []:
            any_law = True
            st.markdown(H(f"""
                <div class="lcard">
                  <div class="lname">{esc(law.get("law"))}</div>
                  <div class="lsec">Section / clause: {esc(law.get("section") or "see guideline text")}</div>
                  <div class="flabel c-amber">Triggered by</div>
                  <div class="ftext" style="margin-bottom:8px">{esc(f.get("pattern"))}</div>
                  <div class="flabel c-pink">How it is violated</div>
                  <div class="ftext">{esc(law.get("how_violated"))}</div>
                </div>"""), unsafe_allow_html=True)
    if not any_law:
        st.info("No legal violations were identified.")


def section_complaint(d, uid):
    comp = d.get("complaint") or {}
    subject = comp.get("subject") or "Complaint regarding deceptive online practices"
    body = (comp.get("body") or "").replace("\\n", "\n")
    st.markdown('<div class="sec c-cyan">📨 Ready-to-file complaint letter</div>', unsafe_allow_html=True)
    st.caption("Replace the [placeholders] with your details, attach your screenshot as evidence, then file it.")
    full = f"Subject: {subject}\n\n{body}"
    st.text_area("Copy-ready complaint", value=full, height=420,
                 label_visibility="collapsed", key=f"complaint_text_{uid}")
    st.download_button("⬇️ Download complaint (.txt)", data=full,
                       file_name="deceptive_guard_complaint.txt", mime="text/plain",
                       key=f"complaint_dl_{uid}")


def section_where(region_key):
    st.markdown('<div class="sec c-amber">🧭 Where to file this complaint</div>', unsafe_allow_html=True)
    for name, desc in FILING.get(region_key, FILING["Global"]):
        st.markdown(f'<div class="portal"><div class="pname">{esc(name)}</div><div class="pdesc">{esc(desc)}</div></div>',
                    unsafe_allow_html=True)
    st.caption("Portal details can change. Confirm on the official website before filing. "
               "This tool gives information, not legal advice.")


def render_report(d, region_key):
    score = max(0, min(100, int(d.get("risk_score") or 0)))
    color, level = risk_style(score)

    st.markdown(H(f"""
        <div class="score-wrap">
          <div class="ring" style="--p:{score};--c:{color}"><div class="ringin">{score}</div></div>
          <div style="flex:1;min-width:260px">
            <div class="lvl" style="--c:{color}">{level}</div>
            <div class="verdict">{esc(d.get("verdict"))}</div>
            <div class="summary">{esc(d.get("summary"))}</div>
            <div class="summary" style="margin-top:8px;color:#fbbf24">Service analysed: {esc(d.get("service_name") or "Unknown")}</div>
          </div>
        </div>"""), unsafe_allow_html=True)

    # First tab shows EVERYTHING; the other tabs jump straight to one section.
    t_all, t_find, t_law, t_comp, t_where = st.tabs([
        "📋 Full Report", "🔍 Findings", "⚖️ Laws", "📨 Complaint", "🧭 Where To File",
    ])
    with t_all:
        section_findings(d)
        section_laws(d)
        section_complaint(d, "all")
        section_where(region_key)
    with t_find:
        section_findings(d)
    with t_law:
        section_laws(d)
    with t_comp:
        section_complaint(d, "tab")
    with t_where:
        section_where(region_key)


# ===================================================================== SIDEBAR
with st.sidebar:
    st.title("🛡️ Deceptive-Guard")
    st.caption("Multimodal Dark Pattern Sentinel v6.0")
    st.markdown("---")
    region_choice = st.selectbox("📍 Regulatory jurisdiction", REGIONS)
    target_lang = st.selectbox("🌐 Report language",
                               ["English", "Kannada", "Hindi", "Spanish", "French", "German"])
    sidebar_key = st.text_input("🔐 Gemini API Key (optional)", type="password")

    api_key = get_key(sidebar_key)
    available_models, model_name = [], ""
    if api_key:
        try:
            available_models = list_models(api_key)
        except Exception as e:
            st.warning(f"Could not list models: {e}")
        if available_models:
            model_name = st.selectbox("🧠 Model (available to your key)", available_models,
                                      index=pick_default(available_models))
        else:
            model_name = st.text_input("🧠 Model name", value="gemini-2.5-flash")
    else:
        st.info("Set GEMINI_API_KEY in .streamlit/secrets.toml or paste it above.")

    if st.session_state.scan_history:
        st.markdown("---")
        st.markdown("### 📊 Session History")
        for i, item in enumerate(reversed(st.session_state.scan_history), 1):
            st.caption(f"{i}. {item}")

region_key = region_choice.split()[0]

# ======================================================================== HERO
st.markdown(H("""
    <div class="hero">
      <span class="badge">Track 1 · PS 01 · Google Gemma Challenge</span>
      <div class="hero-title grad">🛡️ Deceptive-Guard AI: Autonomous UI Threat Sentinel</div>
      <div class="hero-sub">Detect hidden fees, pre-checked boxes, fake countdowns and compliance breaches,
      then get a ready-to-file complaint in seconds.</div>
    </div>"""), unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
cards = [
    (model_name or "no model", "AI Engine"),
    ("&lt; 5s", "Avg Scan Time"),
    (region_key, "Active Ruleset"),
    (str(len(st.session_state.scan_history)), "Scans Conducted"),
]
for col, (val, lbl) in zip((c1, c2, c3, c4), cards):
    col.markdown(f'<div class="mc"><div class="mv">{val}</div><div class="ml">{lbl}</div></div>',
                 unsafe_allow_html=True)

# ===================================================================== UPLOAD
st.markdown('<div class="sec c-cyan">📥 Step 1: Upload interface screenshot</div>', unsafe_allow_html=True)
up = st.file_uploader("Drop your checkout, cart or booking screenshot",
                      type=["jpg", "jpeg", "png"], label_visibility="collapsed")
image = Image.open(up).convert("RGB") if up else None

if image is not None:
    _, mid, _ = st.columns([1, 2, 1])
    mid.image(image, caption="Ingested target UI evidence", use_container_width=True)

    st.markdown('<div class="sec c-pink">🚀 Step 2: Run the audit</div>', unsafe_allow_html=True)
    if st.button("🚀 Run Deceptive-Guard Forensic Audit", use_container_width=True):
        key = get_key(sidebar_key)
        if not key:
            st.error("⚠️ No API key found. Add GEMINI_API_KEY to .streamlit/secrets.toml or paste it in the sidebar.")
        elif not model_name:
            st.error("⚠️ No model selected.")
        else:
            prompt = build_prompt(region_choice, target_lang)
            candidates = [model_name]
            for m in available_models:
                if m != model_name and ("flash" in m or "gemma" in m) and m not in candidates:
                    candidates.append(m)
            candidates = candidates[:4]

            client = genai.Client(api_key=key)
            data, raw_text, used_model, last_error = None, None, None, None
            with st.spinner("Analyzing pixels against regional consumer laws..."):
                for cand in candidates:
                    try:
                        resp = generate(client, cand, prompt, image)
                        raw_text = resp.text
                        data = parse_json(raw_text)
                        if data:
                            used_model = cand
                            break
                    except Exception as e:
                        last_error = e

            if data:
                st.session_state.report = {"data": data, "region_key": region_key, "model": used_model,
                                           "requested": model_name}
                st.session_state.scan_history.append(
                    f"{region_key} · {target_lang} · score {data.get('risk_score', '?')}")
            elif raw_text:
                st.session_state.report = None
                st.warning("The model did not return structured data. Raw output below.")
                st.text_area("Raw output", raw_text, height=300)
            else:
                st.session_state.report = None
                st.error(f"❌ Audit failed: {last_error}")

# Render the saved report (survives reruns, so the download button works)
if st.session_state.report:
    rep = st.session_state.report
    if rep["model"] != rep["requested"]:
        st.caption(f"⚠️ {rep['requested']} could not complete the scan, so {rep['model']} was used instead.")
    st.markdown('<div class="sec grad">🧾 Forensic Audit Report</div>', unsafe_allow_html=True)
    render_report(rep["data"], rep["region_key"])
