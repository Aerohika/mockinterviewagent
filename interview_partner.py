import os
import tempfile
import time

import streamlit as st
from audiorecorder import audiorecorder

import whisper
import pyttsx3
from pydub import AudioSegment
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO

# ================== CONFIG & INIT ================== #
os.environ["STREAMLIT_TELEMETRY_EMAIL"] = ""

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY is missing. Add it to a .env file in this folder.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL_NAME = "gemini-2.5-pro"

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

whisper_model = load_whisper_model()


def init_session():
    if "mode" not in st.session_state:
        st.session_state.mode = "SETUP"
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "history" not in st.session_state:
        st.session_state.history = []      # {"role": "user"/"assistant", "text": str, "audio": bytes}


init_session()


# ================== TTS (pyttsx3) ================== #
def text_to_speech_bytes(text: str) -> bytes:
    """Generate WAV audio bytes from text using offline pyttsx3."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpwav:
        raw_wav = tmpwav.name

    engine.save_to_file(text, raw_wav)
    engine.runAndWait()
    engine.stop()

    audio = AudioSegment.from_file(raw_wav)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fin:
        final_wav = fin.name
    audio.export(final_wav, format="wav")

    with open(final_wav, "rb") as f:
        data = f.read()

    try: os.remove(raw_wav)
    except: pass
    try: os.remove(final_wav)
    except: pass

    return data


# ================== GEMINI HELPERS ================== #
def build_conversation_text(history):
    lines = []
    for m in history:
        prefix = "Candidate" if m["role"] == "user" else "Interviewer"
        lines.append(f"{prefix}: {m['text']}")
    return "\n".join(lines)


def generate_interviewer_reply(history, role):
    system_prompt = f"""
You are a professional job interviewer for the role: {role}.
Rules:
- Ask ONE question at a time.
- Ask follow-ups based on previous answers.
- Mix behavioral, situational, and technical questions.
- Do NOT give feedback during interview.
Always end with a question.
"""
    convo = build_conversation_text(history)
    prompt = system_prompt + "\n\nConversation so far:\n" + convo + "\n\nInterviewer:"
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return f"(Gemini Error: {e})"


def generate_feedback(history, role):
    system_prompt = f"""
You are an expert interview coach. Provide feedback for a mock interview for the role: {role}.
Format strictly:

### 1. Overall Score & Impression
...

### 2. Communication Analysis
...

### 3. Content & Strategy Analysis
...

### 4. Key Areas for Improvement
- 3 actionable tips
"""
    convo = build_conversation_text(history)
    prompt = system_prompt + "\n\nInterview Transcript:\n" + convo + "\n\nFeedback:"
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return f"❌ Could not get feedback: {e}"


# ================== HISTORY ================== #
def add_assistant(text):
    audio = text_to_speech_bytes(text)
    st.session_state.history.append({"role": "assistant", "text": text, "audio": audio})


def add_user(text):
    st.session_state.history.append({"role": "user", "text": text, "audio": None})


def handle_user_answer(text):
    text = text.strip()
    if not text:
        return
    add_user(text)

    lower = text.lower()
    if "end interview" in lower or "feedback" in lower:
        st.session_state.mode = "FEEDBACK"
        st.rerun()

    next_q = generate_interviewer_reply(st.session_state.history, st.session_state.role)
    add_assistant(next_q)
    st.rerun()


def handle_audio_input(audio_segment_or_file):
    if isinstance(audio_segment_or_file, AudioSegment):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp_name = tmp.name
            audio_segment_or_file.export(tmp_name, format="wav")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_segment_or_file.read())
            tmp_name = tmp.name

    with st.spinner("Transcribing audio..."):
        result = whisper_model.transcribe(tmp_name)

    try: os.remove(tmp_name)
    except: pass

    text = result.get("text", "").strip()
    if not text:
        st.warning("Could not understand your answer.")
        return

    st.info(f"📝 Transcribed: **{text}**")
    handle_user_answer(text)


# ================== STREAMLIT UI ================== #
st.set_page_config(page_title="Voice Mock Interview", layout="centered")
st.title("🎤 Voice Mock Interview Agent (Gemini + Whisper)")

# ---------- SETUP ---------- #
if st.session_state.mode == "SETUP":
    st.subheader("Setup your mock interview")
    st.session_state.role = st.text_input("Target role:", value=st.session_state.role)

    if st.button("Start Interview"):
        if not st.session_state.role.strip():
            st.warning("Please enter a role first.")
        else:
            st.session_state.history = []
            st.session_state.mode = "INTERVIEW"
            st.rerun()

# ---------- INTERVIEW ---------- #
elif st.session_state.mode == "INTERVIEW":
    st.subheader(f"Interview — {st.session_state.role}")
    st.write("---")

    # first question
    if len(st.session_state.history) == 0:
        first_q = generate_interviewer_reply(st.session_state.history, st.session_state.role)
        add_assistant(first_q)
        st.rerun()

    # show chat history
    for msg in st.session_state.history:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.markdown(msg["text"])
            if msg["role"] == "assistant" and msg.get("audio"):
                st.audio(msg["audio"], format="audio/wav")

    st.write("---")
    st.markdown("### 🎙 Your turn to answer")

    col1, col2 = st.columns(2)

    # text answer
    with col1:
        text_ans = st.text_input("Type your answer:")
        if st.button("Send Text Answer"):
            handle_user_answer(text_ans)

    # voice answer
    with col2:
        audio = audiorecorder("🎙 Start Recording", "⏹ Stop Recording")
        if len(audio) > 0:
            # 🔥 FIX: Convert audio to bytes before st.audio()
            buf = BytesIO()
            audio.export(buf, format="wav")
            audio_bytes = buf.getvalue()
            st.audio(audio_bytes, format="audio/wav")

            if st.button("Send Voice Answer"):
                handle_audio_input(audio)

    st.write("---")
    if st.button("🛑 End interview & get feedback"):
        st.session_state.mode = "FEEDBACK"
        st.rerun()

# ---------- FEEDBACK ---------- #
elif st.session_state.mode == "FEEDBACK":
    st.subheader("📊 Detailed Interview Feedback")

    with st.spinner("Generating feedback..."):
        feedback = generate_feedback(st.session_state.history, st.session_state.role)

    st.markdown(feedback)

    st.write("---")
    if st.button("🔁 Start New Interview"):
        st.session_state.mode = "SETUP"
        st.session_state.history = []
        st.session_state.role = ""
        st.rerun()