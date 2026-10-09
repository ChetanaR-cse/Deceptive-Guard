import io
import re
from PIL import Image
from google import genai
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Deceptive-Guard | AI Dark Pattern Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Premium Cyber Theme & Neon Typography CSS Engine
css_code = """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap');

html, body, .stApp {
    background-color: #030712 !important;
    color: #e2e8f0 !important;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

#cyber-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
}

p, span, label, li, div {
    font-size: 16px !important;
    line-height: 1.8 !important;
}

h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    color: #00f2fe !important;
    letter-spacing: -0.01em;
}

h2, h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    color: #38bdf8 !important;
    letter-spacing: -0.01em;
}

h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #fbbf24 !important;
}

.block-container {
    position: relative;
    z-index: 1;
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
    margin: 0 auto;
}

[data-testid='stSidebar'] {
    background-color: rgba(6, 9, 17, 0.95) !important;
    border-right: 1px solid #1e293b !important;
    backdrop-filter: blur(12px);
    z-index: 2;
}

.hero-container {
    background: rgba(11, 17, 32, 0.85);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(0, 242, 254, 0.4);
    border-left: 6px solid #00f2fe;
    padding: 32px;
    border-radius: 18px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(0, 242, 254, 0.2);
    margin-bottom: 25px;
}

.badge-tag {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
    color: #030712 !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.metric-card {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.metric-val {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #00f2fe !important;
    font-family: 'JetBrains Mono', monospace;
}

.metric-lbl {
    font-size: 0.85rem !important;
    color: #fbbf24 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 800 !important;
    font-size: 1.15rem !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 4px 25px rgba(0, 114, 255, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%) !important;
    box-shadow: 0 0 30px rgba(0, 198, 255, 0.8) !important;
    transform: translateY(-2px);
}

[data-testid='stFileUploader'] {
    background-color: rgba(15, 23, 42, 0.8) !important;
    border: 2px dashed #00f2fe !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

.stTabs [data-baseweb='tab-list'] {
    gap: 10px;
    background-color: rgba(11, 17, 32, 0.9);
    padding: 8px;
    border-radius: 12px;
    border: 1px solid #1e293b;
}

.stTabs [data-baseweb='tab'] {
    height: 48px;
    border-radius: 8px;
    color: #94a3b8 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

.stTabs [aria-selected='true'] {
    background-color: #1e293b !important;
    color: #00f2fe !important;
}

.card-risk {
    background: rgba(15, 23, 42, 0.92);
    border-left: 6px solid #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(239, 68, 68, 0.25);
}

.card-tricks {
    background: rgba(15, 23, 42, 0.92);
    border-left: 6px solid #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.4);
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(56, 189, 248, 0.25);
}

.card-laws {
    background: rgba(15, 23, 42, 0.92);
    border-left: 6px solid #a855f7;
    border: 1px solid rgba(168, 85, 247, 0.4);
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(168, 85, 247, 0.25);
}

.card-complaint {
    background: rgba(15, 23, 42, 0.92);
    border-left: 6px solid #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.4);
    padding: 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(74, 222, 128, 0.25);
}

.section-title {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
</style>"""

st.markdown(css_code, unsafe_allow_html=True)

# 3. Interactive WebGL/Canvas Matrix Mesh Background Engine
interactive_canvas_js = """
<canvas id="cyber-canvas"></canvas>
<script>
const canvas = document.getElementById('cyber-canvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const particles = [];
const particleCount = 65;
const mouse = { x: null, y: null, radius: 160 };

window.addEventListener('mousemove', (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
});

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.9;
        this.vy = (Math.random() - 0.5) * 0.9;
        this.radius = Math.random() * 2 + 1;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 242, 254, 0.7)';
        ctx.fill();
    }
}

for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        
        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < 130) {
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.strokeStyle = `rgba
