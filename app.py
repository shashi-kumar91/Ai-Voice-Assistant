import os
import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import numpy as np
from faster_whisper import WhisperModel
from voice_service2 import play_text_to_speech, stop_speaking_flag
from ai_assistant import AIVoiceAssistant
from dotenv import load_dotenv

load_dotenv()

assistant = AIVoiceAssistant()
whisper_model = WhisperModel("base.en", device="cpu")

# --------- Utils ---------
def record_audio(duration=5, fs=16000):
    st.info("🎤 Listening for 5 seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio.flatten(), fs

def save_wav(audio_data, fs):
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(f.name, fs, audio_data)
    return f.name

def transcribe(file_path):
    segments, _ = whisper_model.transcribe(file_path)
    return ' '.join([seg.text for seg in segments]).strip()

# --------- UI ----------

st.set_page_config(page_title="Voice Chat Assistant", layout="centered")
st.title("🧠 Voice Chat Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for role, msg in st.session_state.messages:
    st.markdown(f"**{'🧑 You' if role == 'user' else '🤖 Assistant'}**: {msg}")

# Interrupt button
if st.button("🛑 Interrupt / Change Topic"):
    stop_speaking_flag.set()
    st.info("⛔ Speaking stopped. You can start a new topic.")

# Handle transcription from last recording
user_input = ""
if "transcribed_text" in st.session_state:
    user_input = st.session_state.transcribed_text
    del st.session_state.transcribed_text

# Text input
user_input = st.text_input("Type your question or click mic 🎤", value=user_input, key="text_input")

# Record from microphone
if st.button("🎙️ Speak"):
    audio, fs = record_audio()
    path = save_wav(audio, fs)
    st.session_state.transcribed_text = transcribe(path)
    st.rerun()


if user_input:
    stop_speaking_flag.clear()  
    st.session_state.messages.append(("user", user_input))
    response = assistant.interact_with_llm(user_input)
    st.session_state.messages.append(("assistant", response))
    play_text_to_speech(response)
    st.rerun()
