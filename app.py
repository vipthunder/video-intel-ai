
import streamlit as st
from src.video_processor import save_uploaded_video
from src.youtube_processor import download_youtube_video
from src.audio_processor import extract_audio
from src.transcription import transcribe_audio
from src.chunking import chunk_text
from src.vector_store import create_vector_store
from src.retriever import get_retriever
from src.rag_chain import create_rag_chain

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Intelligence",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Background ── */
    .stApp {
        background: #0a0e1a;
        background-image:
            radial-gradient(ellipse 80% 40% at 50% -10%, rgba(99,74,255,0.18) 0%, transparent 70%),
            radial-gradient(ellipse 60% 30% at 80% 80%, rgba(20,200,150,0.10) 0%, transparent 60%);
        min-height: 100vh;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 3rem 4rem;
        max-width: 1100px;
    }

    /* ── Hero title ── */
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(120deg, #fff 30%, #a898ff 70%, #14c896 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.15;
        margin: 0 0 0.4rem;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.05rem;
        color: rgba(255,255,255,0.45);
        font-weight: 300;
        margin-bottom: 2.5rem;
        letter-spacing: 0.2px;
    }

    /* ── Section label ── */
    .section-label {
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: rgba(168,152,255,0.75);
        margin-bottom: 0.6rem;
        display: block;
    }

    /* ── Glass panel ── */
    .glass-panel {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(8px);
    }

    /* ── Status badge ── */
    .badge-idle    { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.45); border: 1px solid rgba(255,255,255,0.1); border-radius: 999px; padding: 3px 14px; font-size: 0.75rem; font-weight: 500; display: inline-block; }
    .badge-success { background: rgba(20,200,150,0.15); color: #14c896; border: 1px solid rgba(20,200,150,0.3); border-radius: 999px; padding: 3px 14px; font-size: 0.75rem; font-weight: 500; display: inline-block; }
    .badge-error   { background: rgba(255,90,90,0.15);  color: #ff6b6b; border: 1px solid rgba(255,90,90,0.3);  border-radius: 999px; padding: 3px 14px; font-size: 0.75rem; font-weight: 500; display: inline-block; }

    /* ── Step log line ── */
    .step-line {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.88rem;
        color: rgba(255,255,255,0.7);
    }
    .step-line:last-child { border-bottom: none; }
    .step-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-top: 5px;
        flex-shrink: 0;
    }
    .dot-done    { background: #14c896; box-shadow: 0 0 8px #14c89640; }
    .dot-running { background: #a898ff; box-shadow: 0 0 8px #a898ff60; animation: pulse 1.2s infinite; }
    .dot-pending { background: rgba(255,255,255,0.18); }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.35; }
    }

    /* ── Streamlit buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #634aff, #a24fe6) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.75rem !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        transition: opacity 0.2s, transform 0.15s !important;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Text inputs / text area ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #fff !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.92rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(99,74,255,0.6) !important;
        box-shadow: 0 0 0 3px rgba(99,74,255,0.15) !important;
    }
    .stTextInput label, .stTextArea label {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.82rem !important;
        font-weight: 400 !important;
    }

    /* ── File uploader ── */
    .stFileUploader > div {
        background: rgba(255,255,255,0.03) !important;
        border: 1.5px dashed rgba(99,74,255,0.4) !important;
        border-radius: 12px !important;
        transition: border-color 0.2s;
    }
    .stFileUploader > div:hover {
        border-color: rgba(99,74,255,0.75) !important;
    }
    .stFileUploader label {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.82rem !important;
    }
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        color: rgba(255,255,255,0.35) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.6) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        color: rgba(255,255,255,0.65) !important;
        font-size: 0.85rem !important;
    }

    /* ── Divider ── */
    hr {
        border: none !important;
        border-top: 1px solid rgba(255,255,255,0.07) !important;
        margin: 2rem 0 !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #634aff !important;
    }

    /* ── Chat messages ── */
    .chat-bubble-user {
        background: linear-gradient(135deg, rgba(99,74,255,0.3), rgba(162,79,230,0.2));
        border: 1px solid rgba(99,74,255,0.3);
        border-radius: 14px 14px 4px 14px;
        padding: 0.85rem 1.1rem;
        margin: 0.5rem 0 0.5rem 3rem;
        color: rgba(255,255,255,0.9);
        font-size: 0.92rem;
        line-height: 1.6;
    }
    .chat-bubble-ai {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px 14px 14px 4px;
        padding: 0.85rem 1.1rem;
        margin: 0.5rem 3rem 0.5rem 0;
        color: rgba(255,255,255,0.82);
        font-size: 0.92rem;
        line-height: 1.6;
    }
    .chat-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .chat-label-user { color: #a898ff; text-align: right; }
    .chat-label-ai   { color: #14c896; }

    /* ── Info chips ── */
    .chip-row {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .chip {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: rgba(255,255,255,0.5);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .chip-dot { width: 6px; height: 6px; border-radius: 50%; }

    /* ── Transcript preview area ── */
    .stTextArea textarea {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.8rem !important;
        line-height: 1.7 !important;
        color: rgba(255,255,255,0.6) !important;
    }

    /* ── Success / error / warning ── */
    .stSuccess {
        background: rgba(20,200,150,0.1) !important;
        border: 1px solid rgba(20,200,150,0.25) !important;
        border-radius: 8px !important;
        color: #14c896 !important;
    }
    .stError {
        background: rgba(255,90,90,0.1) !important;
        border: 1px solid rgba(255,90,90,0.25) !important;
        border-radius: 8px !important;
        color: #ff6b6b !important;
    }
    .stWarning {
        background: rgba(255,180,50,0.1) !important;
        border: 1px solid rgba(255,180,50,0.25) !important;
        border-radius: 8px !important;
        color: #ffb432 !important;
    }

    /* ── Metrics row ── */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    [data-testid="metric-container"] label {
        color: rgba(255,255,255,0.4) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #fff !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,74,255,0.35); border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session State Init ─────────────────────────────────────────────────────────
if "rag_chain" not in st.session_state:
    st.session_state["rag_chain"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []          # list of {"role": "user"|"ai", "text": str}
if "processed_videos" not in st.session_state:
    st.session_state["processed_videos"] = []      # list of video names successfully processed
if "total_chunks" not in st.session_state:
    st.session_state["total_chunks"] = 0

# ── Helper: render a step log ──────────────────────────────────────────────────
def step_log(steps: list[dict]) -> str:
    """steps = [{"label": str, "status": "done"|"running"|"pending"}]"""
    rows = ""
    for s in steps:
        dot_class = {"done": "dot-done", "running": "dot-running", "pending": "dot-pending"}.get(s["status"], "dot-pending")
        rows += f'<div class="step-line"><span class="step-dot {dot_class}"></span><span>{s["label"]}</span></div>'
    return f'<div class="glass-panel" style="padding:1rem 1.25rem;">{rows}</div>'


# ── Core processing function ───────────────────────────────────────────────────
def process_video_file(file_path: str, log_placeholder):
    steps = [
        {"label": "Extracting audio from video…",    "status": "running"},
        {"label": "Transcribing with Whisper…",      "status": "pending"},
        {"label": "Splitting into text chunks…",     "status": "pending"},
        {"label": "Building vector store…",          "status": "pending"},
        {"label": "Initialising retriever…",         "status": "pending"},
        {"label": "Constructing RAG chain…",         "status": "pending"},
    ]

    def refresh(i, new_status):
        steps[i]["status"] = new_status
        if i + 1 < len(steps) and new_status == "done":
            steps[i + 1]["status"] = "running"
        log_placeholder.markdown(step_log(steps), unsafe_allow_html=True)

    log_placeholder.markdown(step_log(steps), unsafe_allow_html=True)

    # Step 0 – audio
    audio_path = extract_audio(file_path)
    refresh(0, "done")

    # Step 1 – transcription
    transcript = transcribe_audio(audio_path)
    refresh(1, "done")

    # Step 2 – chunking
    chunks = chunk_text(transcript)
    refresh(2, "done")

    # Step 3 – vector store
    video_name = file_path.replace("\\", "/").split("/")[-1]

# Save currently active video
    st.session_state["current_video"] = video_name

    vector_store = create_vector_store(chunks, video_name)

    # Step 4 – retriever
    retriever = get_retriever(vector_store, video_name)
    refresh(4, "done")

    # Step 5 – RAG chain
    rag_chain = create_rag_chain(retriever)
    refresh(5, "done")

    st.session_state["rag_chain"] = rag_chain
    st.session_state["processed_videos"].append(video_name)
    st.session_state["total_chunks"] += len(chunks)

    return transcript, chunks


# ═════════════════════
#  LAYOUT

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="hero-title">AI Video Intelligence</h1>'
    '<p class="hero-sub">Upload videos or paste YouTube URLs — ask anything about their content.</p>',
    unsafe_allow_html=True,
)

# Feature chips
processed_count = len(st.session_state["processed_videos"])
status_color = "#14c896" if processed_count > 0 else "rgba(255,255,255,0.2)"
st.markdown(
    f"""
    <div class="chip-row">
        <div class="chip"><span class="chip-dot" style="background:#a898ff;"></span>Multi-video RAG</div>
        <div class="chip"><span class="chip-dot" style="background:#14c896;"></span>Whisper transcription</div>
        <div class="chip"><span class="chip-dot" style="background:#634aff;"></span>YouTube support</div>
        <div class="chip"><span class="chip-dot" style="background:#ff9f5a;"></span>Cross-video Q&A</div>
        <div class="chip"><span class="chip-dot" style="background:{status_color};"></span>
            {processed_count} video{"s" if processed_count != 1 else ""} loaded</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Stats row (only if something processed) ────────────────────────────────────
if processed_count > 0:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Videos Processed", processed_count)
    c2.metric("Text Chunks", st.session_state["total_chunks"])
    c3.metric("Messages", len(st.session_state["chat_history"]))
    c4.metric("Model", "Gemini + Whisper")
    st.markdown("<br>", unsafe_allow_html=True)

# ── Two-column layout ──────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 0.9], gap="large")


# -----------LEFT — INPUT  --------------------------------       
with left_col:
    st.markdown('<span class="section-label"> Video Sources</span>', unsafe_allow_html=True)

    with st.container():
        uploaded_videos = st.file_uploader(
            "Drop video files here",
            type=["mp4", "avi", "mkv", "mov"],
            accept_multiple_files=True,
            help="Supports MP4, AVI, MKV, MOV",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    youtube_urls = st.text_area(
        "YouTube URLs  (one per line)",
        placeholder="https://youtube.com/watch?v=...\nhttps://youtube.com/watch?v=...",
        height=110,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    process_btn = st.button("  Process Videos", use_container_width=True)

    # ── Processing logic ────────────────────────────────────────────────────
    if process_btn:
        urls = [u.strip() for u in (youtube_urls or "").split("\n") if u.strip()]
        total_videos = len(uploaded_videos or []) + len(urls)

        if total_videos == 0:
            st.warning("Please upload a video file or paste at least one YouTube URL.")
        else:
            st.markdown(
                '<span class="section-label" style="margin-top:1.5rem;">⚙️ Processing Pipeline</span>',
                unsafe_allow_html=True,
            )

            # ---- Uploaded files ----
            for video in uploaded_videos or []:
                st.markdown(
                    f'<div style="font-size:0.82rem;color:rgba(255,255,255,0.5);margin-bottom:0.4rem;">'
                    f'Processing <strong style="color:#a898ff;">{video.name}</strong></div>',
                    unsafe_allow_html=True,
                )
                log_ph = st.empty()
                try:
                    file_path = save_uploaded_video(video)
                    transcript, chunks = process_video_file(file_path, log_ph)

                    with st.expander(f"📄 Transcript — {video.name}"):
                        st.text_area("", transcript, height=220, label_visibility="collapsed")

                    with st.expander(f"🧩 Chunks preview — {video.name}"):
                        for idx, chunk in enumerate(chunks[:6], 1):
                            st.markdown(
                                f'<div style="font-size:0.8rem;color:rgba(255,255,255,0.55);'
                                f'border-left:2px solid #634aff;padding-left:10px;margin-bottom:8px;">'
                                f'<span style="color:#634aff;font-weight:600;">#{idx}</span>  {chunk[:260]}…</div>',
                                unsafe_allow_html=True,
                            )
                        if len(chunks) > 6:
                            st.caption(f"…and {len(chunks) - 6} more chunks")

                except Exception as e:
                    st.error(f"Failed to process **{video.name}**: {e}")
                    with st.expander("Error details"):
                        st.exception(e)

            # ---- YouTube URLs ----
            for url in urls:
                short = url[:55] + "…" if len(url) > 55 else url
                st.markdown(
                    f'<div style="font-size:0.82rem;color:rgba(255,255,255,0.5);margin-bottom:0.4rem;">'
                    f'Downloading <strong style="color:#14c896;">{short}</strong></div>',
                    unsafe_allow_html=True,
                )
                log_ph = st.empty()
                try:
                    file_path = download_youtube_video(url)
                    transcript, chunks = process_video_file(file_path, log_ph)

                    video_name = file_path.replace("\\", "/").split("/")[-1]
                    with st.expander(f"📄 Transcript — {video_name}"):
                        st.text_area("", transcript, height=220, label_visibility="collapsed")

                    with st.expander(f"🧩 Chunks — {video_name}"):
                        for idx, chunk in enumerate(chunks[:6], 1):
                            st.markdown(
                                f'<div style="font-size:0.8rem;color:rgba(255,255,255,0.55);'
                                f'border-left:2px solid #14c896;padding-left:10px;margin-bottom:8px;">'
                                f'<span style="color:#14c896;font-weight:600;">#{idx}</span>  {chunk[:260]}…</div>',
                                unsafe_allow_html=True,
                            )
                        if len(chunks) > 6:
                            st.caption(f"…and {len(chunks) - 6} more chunks")

                except Exception as e:
                    st.error(f"Failed to download: {e}")
                    with st.expander("Error details"):
                        st.exception(e)
            st.info( "Local video uploads are fully supported.YouTube downloads may be restricted in cloud deployments.")

            st.success(f"  {total_videos} video(s) processed and ready for Q&A.")


# Right-chat
with right_col:
    st.markdown('<span class="section-label">💬 Knowledge Chat</span>', unsafe_allow_html=True)

    # Status badge
    if st.session_state["rag_chain"] is None:
        st.markdown(
            '<span class="badge-idle">Process videos to unlock chat</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="badge-success">● Ready to answer questions</span>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat history bubble rendering ──────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        if not st.session_state["chat_history"]:
            st.markdown(
                '<div style="text-align:center;padding:2.5rem 1rem;color:rgba(255,255,255,0.2);'
                'font-size:0.88rem;border:1px dashed rgba(255,255,255,0.07);border-radius:12px;">'
                '✦  Ask anything once your videos are processed</div>',
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-label chat-label-user">You</div>'
                        f'<div class="chat-bubble-user">{msg["text"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="chat-label chat-label-ai">AI</div>'
                        f'<div class="chat-bubble-ai">{msg["text"]}</div>',
                        unsafe_allow_html=True,
                    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Input row ──────────────────────────────────────────────────────────
    q_col, btn_col = st.columns([4, 1], gap="small")

    with q_col:
        question = st.text_input(
            "Your question",
            placeholder="e.g. Summarise the key points from the videos…",
            label_visibility="collapsed",
            disabled=(st.session_state["rag_chain"] is None),
            key="question_input",
        )

    with btn_col:
        send_btn = st.button(
            "Ask",
            use_container_width=True,
            disabled=(st.session_state["rag_chain"] is None),
        )

    # ── Clear chat ─────────────────────────────────────────────────────────
    if st.session_state["chat_history"]:
        if st.button("🗑  Clear chat history", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

    # ── Answer logic ───────────────────────────────────────────────────────
    if send_btn and question and st.session_state["rag_chain"]:
        # Append user message
        st.session_state["chat_history"].append({"role": "user", "text": question})

        with st.spinner("Thinking…"):
            try:
                answer = st.session_state["rag_chain"].invoke({"question": question})
                answer_text = str(answer)
            except Exception as e:
                answer_text = f"⚠️ Error generating answer: {e}"

        # Append AI message
        st.session_state["chat_history"].append({"role": "ai", "text": answer_text})
        st.rerun()
