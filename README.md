# 🧠 AI Voice Assistant

A real-time voice-enabled assistant built with Python that listens to your speech, transcribes it using Whisper, processes it via LLaMA 3 (Groq API), and responds back in natural voice using TTS. Includes support for live interruption, making conversations more human-like.

---

## 🎯 Features

- 🎙️ **Speech-to-Text**: Converts user voice input to text using [Whisper](https://github.com/openai/whisper).
- 🤖 **AI Responses**: Sends input to a Large Language Model (LLaMA 3 via Groq API) and returns a relevant reply.
- 🔊 **Text-to-Speech**: Converts AI response back to speech using `gTTS` and `pygame`.
- ⛔ **Interruptible Output**: Stop speech mid-way and change the topic using an interrupt button.
- 🌐 **User Interface**: Clean web UI built using [Streamlit](https://streamlit.io/).

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Speech-to-Text**: Whisper (via `faster-whisper`)
- **LLM Integration**: LLaMA 3 via Groq API
- **Text-to-Speech**: gTTS + pygame (fallback for reliability)
- **Audio Handling**: PyAudio, SoundDevice, threading
- **Language**: Python

---

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/shashi-kumar91/AI-Voice-Assistant.git
cd AI-Voice-Assistant

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
