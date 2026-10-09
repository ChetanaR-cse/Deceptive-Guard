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
.stApp p, .stApp label, .stApp li, .stApp span {font-family:'Plus Jakarta Sans',sans-serif;}
.stApp label, .stApp .stMarkdown p {color:#cbd5e1; font-size:16px;}
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
.flabe
