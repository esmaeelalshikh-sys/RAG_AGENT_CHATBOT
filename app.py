import streamlit as st
import re
import os
from dotenv import load_dotenv

# ---------------------------
# 1. الربط مع الوكيل (Agent)
# ---------------------------
try:
    # محاولة الاستدعاء بناءً على هيكلية المجلدات التي ظهرت في الصور (agent/agent.py)
    from agent.agent import SimpleAgent
    AGENT_AVAILABLE = True
except ImportError:
    try:
        from agent import SimpleAgent
        AGENT_AVAILABLE = True
    except ImportError:
        AGENT_AVAILABLE = False

# ---------------------------
# 2. الإعدادات والتنسيق (Styling)
# ---------------------------
st.set_page_config(
    page_title="Syrian Universities Assistant",
    page_icon="🎓",
    layout="centered"
)

COLORS = {
    "bg_dark": "#161616",
    "card_bg": "#3d3a3b",
    "text_light": "#edebe0",
    "accent_gold": "#b9a779",
    "accent_gold_dark": "#988561",
    "muted": "#8a8a8a",
    "danger": "#6b1f2a",
    "success": "#054239",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif !important; }}
.stApp {{ background-color: {COLORS['bg_dark']}; color: {COLORS['text_light']}; }}
h1, h2, h3 {{ color: {COLORS['accent_gold']} !important; }}
[data-testid="stChatMessage"] {{
    background-color: {COLORS['card_bg']};
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}}
[data-testid="stChatMessageUser"] {{ border-right: 4px solid {COLORS['accent_gold_dark']}; }}
[data-testid="stChatMessageAssistant"] {{ border-left: 4px solid {COLORS['accent_gold']}; }}
.eval-box {{
    margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.2);
    border-radius: 8px; border-top: 1px solid rgba(255,255,255,0.1);
}}
.progress-bg {{ background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; margin: 8px 0; overflow: hidden; }}
.progress-fill {{ height: 100%; border-radius: 4px; transition: width 0.5s ease; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 3. الوظائف المساعدة (Logic)
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "en" # لغة الواجهة فقط

if "agent" not in st.session_state and AGENT_AVAILABLE:
    try:
        st.session_state.agent = SimpleAgent()
    except Exception as e:
        st.error(f"Failed to initialize Agent: {e}")

def detect_language(text):
    """يكتشف إذا كان النص يحتوي على حروف عربية."""
    return "ar" if any('\u0600' <= char <= '\u06FF' for char in text) else "en"

def parse_evaluation(eval_text):
    score = 0
    reason = "No detailed reason provided."
    score_match = re.search(r'(?:Score|النتيجة|التقييم)\s*[:\-]?\s*(\d)', eval_text, re.IGNORECASE)
    if score_match: score = int(score_match.group(1))
    
    if "Reason:" in eval_text: reason = eval_text.split("Reason:", 1)[1].strip()
    elif "السبب:" in eval_text: reason = eval_text.split("السبب:", 1)[1].strip()
    return score, reason

def render_evaluation_card(score, reason, lang):
    percentage = min(score * 20, 100)
    bar_color = COLORS['success'] if score >= 4 else ("#d4a017" if score == 3 else COLORS['danger'])
    label = "CONFIDENCE SCORE" if lang == 'en' else "درجة الثقة"
    
    st.markdown(f"""
    <div class="eval-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{COLORS['accent_gold']}; font-weight:bold; font-size:0.9em;">{label}</span>
            <span style="color:{COLORS['text_light']}; font-weight:bold;">{score}/5</span>
        </div>
        <div class="progress-bg"><div class="progress-fill" style="width:{percentage}%; background-color:{bar_color};"></div></div>
        <div style="font-size:0.85em; color:{COLORS['muted']}; margin-top:5px;">{reason}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# 4. واجهة المستخدم (UI)
# ---------------------------

col_title, col_btn = st.columns([5, 1])
with col_title:
    if st.session_state.lang == "en":
        st.title("Informatics Engineering Bot")
        st.caption("Official Syrian University Documents Assistant")
    else:
        st.title("بوت الهندسة المعلوماتية")
        st.caption("مساعد الوثائق الرسمية للجامعات السورية")

with col_btn:
    if st.button("العربية" if st.session_state.lang == "en" else "English"):
        st.session_state.lang = "ar" if st.session_state.lang == "en" else "en"
        st.rerun()

st.markdown("---")

# عرض سجل الدردشة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "evaluation" in msg:
            s, r = parse_evaluation(msg["evaluation"])
            render_evaluation_card(s, r, msg.get("query_lang", "en"))

# الإدخال والمعالجة
input_label = "Type your question..." if st.session_state.lang == "en" else "أدخل سؤالك هنا..."
if prompt := st.chat_input(input_label):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # كشف لغة السؤال لإجبار البوت على الرد بنفس اللغة
    query_lang = detect_language(prompt)

    with st.chat_message("assistant"):
        if not AGENT_AVAILABLE:
            st.error("Agent module not found.")
        else:
            with st.spinner("Thinking..." if query_lang == "en" else "جاري التفكير..."):
                try:
                    # نرسل query_lang المكتشفة من النص وليس لغة الواجهة
                    answer, evaluation = st.session_state.agent.ask(prompt, query_lang)
                    
                    st.markdown(answer)
                    s, r = parse_evaluation(evaluation)
                    render_evaluation_card(s, r, query_lang)

                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer, 
                        "evaluation": evaluation,
                        "query_lang": query_lang
                    })
                except Exception as e:
                    st.error(f"Error: {e}")