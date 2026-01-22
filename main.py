import os
import time
from tts.engine import TTSEngine
from config.settings import AUDIO_DIR

def main():
    try:
        engine = TTSEngine()
        
        while True:
            print("\n--- VocalMind ---")
            print("Select Voice Gender:")
            print("1. Male")
            print("2. Female")
            print("Q. Quit")
            
            choice = input("Enter choice (1/2/Q): ").strip()
            
            if choice.lower() == 'q':
                print("Exiting...")
                break
                
            if choice not in ['1', '2']:
                print("Invalid selection. Please press 1 or 2.")
                continue
                
            text = input("Enter text to generate audio: ").strip()
            if not text:
                print("Text cannot be empty.")
                continue
                
            timestamp = int(time.time())
            filename = f"output_{timestamp}.wav"
            filepath = os.path.join(AUDIO_DIR, filename)
            
            print("Generating audio...")
            try:
                engine.generate_audio(text, choice, filepath)
                print(f"Audio saved successfully: {filepath}")
            except Exception as e:
                print(f"Error generating audio: {e}")
                
            # Optional: Ask to play or continue? (Not in requirements, just repeat loop)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
