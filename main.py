import os
import time
import warnings
import logging

# Suppress warnings and logs for a cleaner terminal
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger("TTS").setLevel(logging.ERROR)

from tts.engine import TTSEngine
from config.settings import AUDIO_DIR
from utils import validate_input

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
            if not validate_input(text):
                print("Text cannot be empty.")
                continue
                
            timestamp = int(time.time())
            filename = f"output_{timestamp}.wav"
            filepath = os.path.join(AUDIO_DIR, filename)
            
            print("Generating audio...")
            gender_map = {'1': 'male', '2': 'female'}
            selected_gender = gender_map.get(choice, 'male') # Default to male if something goes wrong, though valid input checked above
            
            try:
                engine.generate_audio(text, selected_gender, filepath)
                print("audio generation is successful")
                
            except Exception as e:
                print(f"Error generating audio: {e}")
                
            # Loop continues...
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
