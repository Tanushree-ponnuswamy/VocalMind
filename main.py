import os
import time
import warnings
import logging

# Suppress logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

from tts.engine import TTSEngine
from config.settings import AUDIO_DIR

def main():
    try:
        engine = TTSEngine()
        
        while True:
            print("\n--- VocalMind (Standard TTS) ---")
            print("1. Male Voice")
            print("2. Female Voice")
            print("Q. Quit")
            
            choice = input("Select an option: ").strip().lower()
            
            if choice == 'q':
                break
                
            if choice not in ['1', '2']:
                print("Invalid selection.")
                continue

            gender = "male" if choice == '1' else "female"
            
            print("Enter text (or type 'FILE' to read script.txt). Press Enter twice to finish:")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            
            text = "\n".join(lines).strip()
            
            if text.upper() == "FILE":
                if os.path.exists("script.txt"):
                    with open("script.txt", "r") as f:
                        text = f.read().strip()
                else:
                    print("script.txt not found.")
                    continue

            if not text:
                continue
                
            timestamp = int(time.time())
            filepath = os.path.join(AUDIO_DIR, f"output_{timestamp}.wav")
            
            print(f"\nGenerating audio for: {text[:50]}...")

            try:
                engine.generate_audio(text, gender, filepath)
                print(f"Done! Saved to: {filepath}")
            except Exception as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
