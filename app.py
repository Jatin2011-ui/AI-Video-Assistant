import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="VidMind AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0A0A0F;
    color: #E8E6F0;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #1a0a3a 0%, #0A0A0F 60%);
}

/* hide streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 72px 24px 48px;
    position: relative;
}

.hero-eyebrow {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9B7FE8;
    border: 1px solid #2D1F5E;
    border-radius: 100px;
    padding: 6px 16px;
    margin-bottom: 28px;
    background: rgba(155, 127, 232, 0.08);
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(48px, 7vw, 88px);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.03em;
    color: #F0EEF8;
    margin-bottom: 20px;
}

.hero-title span {
    background: linear-gradient(135deg, #9B7FE8 0%, #C4A8FF 50%, #7EB8FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 17px;
    font-weight: 300;
    color: #8A879A;
    max-width: 480px;
    margin: 0 auto 48px;
    line-height: 1.6;
}

/* ── Input card ── */
.input-shell {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 24px 64px;
}

/* Streamlit input overrides */
[data-testid="stTextInput"] input {
    background: #12111A !important;
    border: 1px solid #2A2640 !important;
    border-radius: 14px !important;
    color: #E8E6F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    padding: 18px 20px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #9B7FE8 !important;
    box-shadow: 0 0 0 3px rgba(155, 127, 232, 0.15) !important;
}

[data-testid="stTextInput"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #6B6880 !important;
    margin-bottom: 8px !important;
}

/* selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #12111A !important;
    border: 1px solid #2A2640 !important;
    border-radius: 14px !important;
    color: #E8E6F0 !important;
}

[data-testid="stSelectbox"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #6B6880 !important;
}

/* ── Primary button ── */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #7B5FD4, #9B7FE8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 18px 32px !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    margin-top: 8px !important;
}

[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Progress / status ── */
[data-testid="stStatus"] {
    background: #12111A !important;
    border: 1px solid #2A2640 !important;
    border-radius: 14px !important;
}

/* ── Results area ── */
.results-wrap {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px 80px;
}

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(26px, 4vw, 42px);
    font-weight: 800;
    color: #F0EEF8;
    margin-bottom: 40px;
    text-align: center;
    letter-spacing: -0.02em;
}

.result-title em {
    font-style: normal;
    background: linear-gradient(135deg, #9B7FE8, #7EB8FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Cards ── */
.card {
    background: #12111A;
    border: 1px solid #1E1C2E;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #9B7FE8, #7EB8FF);
    opacity: 0;
    transition: opacity 0.3s;
}

.card:hover::before { opacity: 1; }

.card-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9B7FE8;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1E1C2E;
}

.card-body {
    font-size: 15px;
    line-height: 1.75;
    color: #B8B4CC;
    font-weight: 300;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #12111A !important;
    border: 1px solid #1E1C2E !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 4px !important;
    margin-bottom: 24px !important;
}

[data-testid="stTabs"] [role="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #6B6880 !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    border: none !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #1E1C2E !important;
    color: #E8E6F0 !important;
}

/* ── Chat ── */
.chat-wrap {
    max-width: 760px;
    margin: 0 auto;
}

.chat-bubble-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 16px;
}

.chat-bubble-user .bubble {
    background: linear-gradient(135deg, #7B5FD4, #9B7FE8);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 14px 20px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.6;
}

.chat-bubble-ai {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 16px;
}

.chat-bubble-ai .bubble {
    background: #12111A;
    border: 1px solid #1E1C2E;
    color: #B8B4CC;
    border-radius: 18px 18px 18px 4px;
    padding: 14px 20px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.6;
}

.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #9B7FE8, #7EB8FF);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    margin-right: 10px;
    flex-shrink: 0;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #1E1C2E;
    margin: 40px 0;
}

/* ── Transcript expand ── */
[data-testid="stExpander"] {
    background: #12111A !important;
    border: 1px solid #1E1C2E !important;
    border-radius: 14px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    color: #6B6880 !important;
}

/* spinner */
[data-testid="stSpinner"] { color: #9B7FE8 !important; }

</style>
""", unsafe_allow_html=True)


# ── Session state ──
if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False


# ══════════════════════════════════════════
# HERO
# ══════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ &nbsp; AI Video Intelligence</div>
    <div class="hero-title">Turn any video into<br><span>actionable insight</span></div>
    <div class="hero-sub">Paste a YouTube link. Get a transcript, summary, action items, and a chat interface — in minutes.</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# INPUT
# ══════════════════════════════════════════
with st.container():
    st.markdown('<div class="input-shell">', unsafe_allow_html=True)

    source = st.text_input(
        "Video source",
        placeholder="https://youtube.com/watch?v=...",
        label_visibility="visible"
    )

    lang = st.selectbox(
        "Language",
        ["English", "Hinglish"],
        label_visibility="visible"
    )

    run = st.button("⚡  Analyse Video", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# PIPELINE
# ══════════════════════════════════════════
if run and source:
    st.session_state.chat_history = []
    st.session_state.result = None

    with st.status("Working on it...", expanded=True) as status:
        try:
            from utils.audio_processor import process_input
            st.write("🎵 Downloading & extracting audio...")
            chunks = process_input(source)

            from core.transcriber import transcribe_all
            st.write(f"🎙️ Transcribing {len(chunks)} chunk(s) with Whisper...")
            transcript = transcribe_all(chunks, lang)

            from core.summarizer import summarize, generate_title
            st.write("✍️ Generating title & summary...")
            title = generate_title(transcript)
            summary = summarize(transcript)

            from core.extractor import extract_action_items, extract_key_decisions, extract_questions
            st.write("🔍 Extracting insights...")
            action_items = extract_action_items(transcript)
            decisions = extract_key_decisions(transcript)
            questions = extract_questions(transcript)

            from core.rag_engine import build_rag_chain
            st.write("🧠 Building knowledge base...")
            rag_chain = build_rag_chain(transcript)

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            status.update(label="✅ Done!", state="complete", expanded=False)

        except Exception as e:
            status.update(label="❌ Something went wrong", state="error")
            st.error(f"{e}")


# ══════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════
if st.session_state.result:
    r = st.session_state.result

    st.markdown('<div class="results-wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="result-title"><em>{r["title"]}</em></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋  Insights", "💬  Chat", "📄  Transcript"])

    # ── Tab 1: Insights ──
    with tab1:
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">🗒 Summary</div>
                <div class="card-body">{r["summary"]}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">
                <div class="card-label">❓ Open Questions</div>
                <div class="card-body">{r["open_questions"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">✅ Action Items</div>
                <div class="card-body">{r["action_items"]}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">
                <div class="card-label">🏛 Key Decisions</div>
                <div class="card-body">{r["key_decisions"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Chat ──
    with tab2:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

        # render history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-bubble-user">
                    <div class="bubble">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble-ai">
                    <div class="avatar">🤖</div>
                    <div class="bubble">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)

        question = st.chat_input("Ask anything about this video...")
        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                from core.rag_engine import ask_question
                answer = ask_question(r["rag_chain"], question)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 3: Transcript ──
    with tab3:
        with st.expander("Full transcript", expanded=False):
            st.markdown(f'<div class="card-body" style="white-space:pre-wrap">{r["transcript"]}</div>',
                        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Empty state ──
elif not run:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 60px; color: #2E2B40; font-size:13px; letter-spacing:0.05em;">
        PASTE A LINK ABOVE TO BEGIN
    </div>
    """, unsafe_allow_html=True)