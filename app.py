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
css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, .stApp {
    background-color: #05070e !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(0, 242, 254, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(112, 0, 255, 0.08) 0px, transparent 50%);
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
}

p, span, label, h1, h2, h3, h4, h5, h6, div {
    color: #e2e8f0;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
    margin: 0 auto;
}

[data-testid="stSidebar"] {
    background-color: #070a12 !important;
    border-right: 1px solid #1e293b !important;
}

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

[data-testid="stFileUploader"] {
    background-color: #0b1120 !important;
    border: 2px dashed #1e293b !important;
    border-radius: 14px !important;
    padding: 18px !important;
}

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
