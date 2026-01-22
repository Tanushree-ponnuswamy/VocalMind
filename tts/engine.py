import pyttsx3
from tts.voices import get_voice_id_by_gender

class TTSEngine:
    def __init__(self):
        print("Initializing Standard TTS Engine...")
        # We do NOT initialize self.engine here because pyttsx3 on Windows
        # has issues with event loops if reused across multiple runAndWait calls
        # in an interactive loop. We initialize it per-generation instead.

    def generate_audio(self, text, gender_input, output_filename):
        # Initialize a fresh engine instance for each run to avoid event loop hanging issues
        # This is required for pyttsx3 to work reliably in a loop
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)

        # Get Voice ID based on gender selection
        voice_id = get_voice_id_by_gender(engine, gender_input)
        
        # Set the voice
        if voice_id:
            engine.setProperty('voice', voice_id)
            print(f"Selected voice: {voice_id}")
        else:
            print("Voice not found, using default.")
        
        print(f"Synthesizing text...")
        
        try:
            # Save to file
            engine.save_to_file(text, output_filename)
            engine.runAndWait()
        finally:
            # Explicit cleanup
            if hasattr(engine, 'stop'):
               engine.stop()
            del engine
        
        return output_filename
