import os
import sys
from tts.engine import TTSEngine
from config.settings import AUDIO_DIR

def run_test():
    print("Starting test run...")
    try:
        engine = TTSEngine()
        print("Engine initialized.")
        
        text = " In the ancient land of Eldoria, where skies shimmered and forests, whispered secrets to the wind, lived a dragon named Zephyros.  Not the 'burn it all down' kind...  but he was gentle, wise, with eyes like old stars.  Even the birds fell silent when he passed. He spent his days cataloging the clouds and learning the songs of the crickets, for he knew that every sound held a story worth remembering."
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
