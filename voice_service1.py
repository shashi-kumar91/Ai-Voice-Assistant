# voice_service1.py
import threading
import playsound
from gtts import gTTS
import os
import tempfile
import shutil
import pygame  # Fallback audio library

# Global event to control speech interruption
speech_active = threading.Event()
speech_active.set()

def stop_speech():
    """Stop the current speech playback."""
    speech_active.clear()
    pygame.mixer.music.stop()  # Stop pygame playback if active

def play_text_to_speech(text, event=speech_active):
    """Play text-to-speech with interruption support."""
    try:
        # Initialize pygame mixer
        pygame.mixer.init()

        # Use a custom temp directory with write permissions
        temp_dir = tempfile.gettempdir()
        if not os.access(temp_dir, os.W_OK):
            temp_dir = os.path.join(os.path.expanduser("~"), "temp")
            os.makedirs(temp_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=temp_dir) as fp:
            tts = gTTS(text=text, lang='en')
            tts.save(fp.name)
            print(f"Audio file saved at: {fp.name}")  # Debug: Confirm file creation

            def play():
                if event.is_set():
                    try:
                        playsound.playsound(fp.name, block=False)
                        while playsound._playsoundWin.is_playing(fp.name):
                            if not event.is_set():
                                playsound._playsoundWin.stop(fp.name)
                                break
                    except Exception as e:
                        print(f"playsound failed: {e}")
                        # Fallback to pygame
                        pygame.mixer.music.load(fp.name)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy() and event.is_set():
                            pass

            thread = threading.Thread(target=play)
            thread.start()
            thread.join(timeout=10)  # Limit join to 10 seconds to prevent hanging
            os.unlink(fp.name)  # Clean up the file
        return not event.is_set()  # Return True if interrupted
    except Exception as e:
        print(f"Error in play_text_to_speech: {e}")
        return False

# Initialize pygame at module level (optional, for better resource management)
pygame.mixer.quit()  # Ensure clean slate
pygame.mixer.init()