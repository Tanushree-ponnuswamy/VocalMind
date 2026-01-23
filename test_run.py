import os
import sys
from tts.engine import TTSEngine
from config.settings import AUDIO_DIR

def run_test():
    print("Starting test run...")
    try:
        engine = TTSEngine()
        print("Engine initialized.")
        
        text = "Hello, checking the voice quality."
        gender = "male"
        output_file = os.path.join(AUDIO_DIR, "test_output.wav")
        
        print(f"Generating audio for text: '{text}' with gender: {gender}")
        engine.generate_audio(text, gender, output_file)
        print(f"Success! Output saved to: {output_file}")
    except Exception as e:
        error_msg = f"Test failed with error: {e}"
        print(error_msg)
        with open("error.log", "w") as f:
            f.write(error_msg)
            import traceback
            traceback.print_exc(file=f)

if __name__ == "__main__":
    run_test()
