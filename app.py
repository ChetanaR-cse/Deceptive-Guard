import io
import re
from PIL import Image
from google import genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Deceptive-Guard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Premium Cyber Dark Theme CSS Engine
css_lines = [
    "<style>",
    "@import url('https://fonts.googleapis.com/"
    "css2?family=Plus+Jakarta+Sans:wght@400;500;600;"
    "700;800&family=JetBrains+Mono:wght@600;800&"
    "display=swap');",
    "html, body, .stApp {",
    " background-color: #030712 !important;",
    " background-image: radial-gradient(at 0% 0%, "
    "rgba(0, 242, 254, 0.15) 0px, transparent 50%), "
    "radial-gradient(at 100% 100%, "
    "rgba(124, 58, 237, 0.15) 0px, transparent 50%) "
    "!important;",
    " color: #f8fafc !important;",
    " font-family: 'Plus Jakarta Sans', sans-serif;",
    "}",
    "p, span, label, li, div {",
    " color: #e2e8f0 !important;",
    " font-size: 16px !important;",
    " line-height: 1.8 !important;",
    "}",
    "h1 {",
    " font-family: 'Plus Jakarta Sans', sans-serif "
    "!important;",
    " font-weight: 800 !important;",
    " color: #00f2fe !important;",
    " letter-spacing: -0.01em;",
    "}",
    "h2, h3 {",
    " font-family: 'Plus Jakarta Sans', sans-serif "
    "!important;",
    " font-weight: 800 !important;",
    " color: #38bdf8 !important;",
    " letter-spacing: -0.01em;",
    "}",
    "h4, h5, h6 {",
    " font-family: 'Plus Jakarta Sans', sans-serif "
    "!important;",
    " font-weight: 700 !important;",
    " color: #fbbf24 !important;",
    "}",
    ".block-container {",
    " position: relative;",
    " z-index: 1;",
    " max-width: 1250px;",
    " padding-top: 1.5rem;",
    " padding-bottom: 4rem;",
    " margin: 0 auto;",
    "}",
    "[data-testid='stSidebar'] {",
    " background-color: rgba(6, 9, 17, 0.95) "
    "!important;",
    " border-right: 1px solid #1e293b !important;",
    " backdrop-filter: blur(12px);",
    " z-index: 2;",
    "}",
    ".hero-container {",
    " background: rgba(11, 17, 32, 0.85);",
    " backdrop-filter: blur(16px);",
    " border: 1px solid rgba(0, 242, 254, 0.4);",
    " border-left: 6px solid #00f2fe;",
    " padding: 32px;",
    " border-radius: 18px;",
    " box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), "
    "0 0 25px rgba(0, 242, 254, 0.2);",
    " margin-bottom: 25px;",
    "}",
    ".badge-tag {",
    " background: linear-gradient(90deg, #00f2fe 0%, "
    "#4facfe 100%);",
    " color: #030712 !important;",
    " padding: 6px 16px;",
    " border-radius: 20px;",
    " font-size: 12px !important;",
    " font-weight: 800 !important;",
    " text-transform: uppercase;",
    " letter-spacing: 0.08em;",
    "}",
    ".metric-card {",
    " background: rgba(15, 23, 42, 0.85);",
    " backdrop-filter: blur(12px
