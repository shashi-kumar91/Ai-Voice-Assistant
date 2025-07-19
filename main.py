import os
import wave
import pyaudio
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel

from voice_service import play_text_to_speech
from ai_assistant import AIVoiceAssistant

# Setup
model = WhisperModel("base.en", device="cuda" if os.environ.get("USE_CUDA") else "cpu")
assistant = AIVoiceAssistant()

# Audio config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 4
TEMP_FILE = "input.wav"

def is_silence(audio_data, threshold=3000):
    max_amp = np.max(np.abs(audio_data))
    return max_amp <= threshold

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    frames = []

    print("🎤 Listening... Speak now!")

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(TEMP_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe():
    segments, _ = model.transcribe(TEMP_FILE)
    text = ' '.join([seg.text for seg in segments])
    return text.strip()

def main():
    try:
        while True:
            record_audio()
            rate, data = wavfile.read(TEMP_FILE)
            if is_silence(data):
                print("🧘 Detected silence. Skipping...")
                continue

            user_text = transcribe()
            print(f"🗣️  You said: {user_text}")

            response = assistant.interact_with_llm(user_text)
            print(f"🤖 Assistant: {response}")

            play_text_to_speech(response)
            os.remove(TEMP_FILE)

    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

if __name__ == "__main__":
    main()
