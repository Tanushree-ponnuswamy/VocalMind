import os
import torch

# Workaround for Coqui TTS with PyTorch 2.6+ which defaults weights_only=True
# This causes issues with loading legacy checkpoints used by XTTS
original_load = torch.load

def safe_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_load(*args, **kwargs)

torch.load = safe_load

import torchaudio
import soundfile as sf

# Monkey-patch torchaudio.load to force use of soundfile directly
# This entirely bypasses torchaudio's internal loading which is broken on some setups
def _safe_audio_load(filepath, *args, **kwargs):
    # Ignore backend arg if present
    
    # Load using soundfile
    data, samplerate = sf.read(filepath, dtype='float32')
    
    # Convert start/end if necessary? XTTS usually loads full file for speaker encoder.
    # XTTS might pass 'frame_offset' or 'num_frames', but let's assume valid full load if it's for speaker clone.
    
    tensor = torch.from_numpy(data)
    
    # Ensure (channels, frames) format
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    else:
        # soundfile is (frames, channels), torchaudio expects (channels, frames)
        tensor = tensor.t()
        
    return tensor, samplerate

torchaudio.load = _safe_audio_load

from TTS.api import TTS

class TTSEngine:
    def __init__(self):
        # Redirect stdout/stderr to supress the "Initializing..." banner and loading bars
        # This is a bit hacky but effective for Coqui TTS which is very verbose
        import sys
        
        # Save original streams
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        try:
            # Mute
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
            
            self.tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                gpu=False
            )
        finally:
            # Restore
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def generate_audio(self, text, gender_input, output_filename):
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)

        # Ensure text ends with punctuation to help the model finish the sentence
        text = text.strip()
        if not text.endswith(('.', '!', '?')):
            text += "."

        speaker_wav = (
            "samples/male.wav"
            if gender_input.lower() == "male"
            else "samples/female.wav"
        )
        
        if not os.path.exists(speaker_wav):
            print(f"ERROR: Sample file not found at {speaker_wav}")

        # Redirect stdout to suppress "Text splitted to sentences" and processing time logs
        import sys
        original_stdout = sys.stdout
        try:
            sys.stdout = open(os.devnull, 'w')
            
            # XTTS v2 inference
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language="en",
                file_path=output_filename,
                split_sentences=True, 
                temperature=0.4,      # Lowered for better pronunciation stability
                top_k=50,             # Limit vocabulary to top 50 likely tokens
                top_p=0.8,            # Nucleus sampling for better coherence
                do_sample=True
            )
        finally:
            sys.stdout = original_stdout

        return output_filename
