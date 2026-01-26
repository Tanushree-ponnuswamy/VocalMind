import re
import io
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from kokoro import KPipeline
from scipy.signal import butter, lfilter

class TTSEngine:
    def __init__(self):
        print("Starting Enhanced Kokoro TTS Engine")
        # Initialize the Kokoro Pipeline
        self.pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
        self.sample_rate = 24000
        self.voices = {"female": "af_bella", "male": "am_michael"}

    def _apply_whisper_filter(self, audio):
        """Removes low-end bass and adds breathy noise for natural whispering."""
        stop_freq = 500 
        nyquist = 0.5 * self.sample_rate
        high = stop_freq / nyquist
        b, a = butter(4, high, btype='high')
        audio = lfilter(b, a, audio)
        # Add subtle white noise for the 'breath' effect
        noise = np.random.normal(0, 0.001, len(audio))
        return audio + noise

    def apply_dsp(self, audio, pitch=0, speed=1.0, is_whisper=False):
        if hasattr(audio, "detach"):
            audio = audio.detach().cpu().numpy()

        if is_whisper:
            audio = self._apply_whisper_filter(audio)

        if speed != 1.0:
            audio = librosa.effects.time_stretch(audio, rate=speed)

        if pitch != 0:
            audio = librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=pitch)

        return audio

    def to_segment(self, audio):
        buf = io.BytesIO()
        sf.write(buf, audio, self.sample_rate, format="WAV")
        buf.seek(0)
        return AudioSegment.from_wav(buf)

    def parse_text(self, text):
        """
        Splits text into chunks. 
        Example: "Hello [whispers] stay quiet" -> [("normal", "Hello"), ("whispers", "stay quiet")]
        """
        # This regex looks for text BEFORE a tag, or text AFTER the last tag
        pattern = re.compile(r'([^\[]+)(?:\[(sarcastically|whispers|giggles)\])?', re.I)
        matches = pattern.findall(text)
        
        parts = []
        for content, tag in matches:
            content = content.strip()
            if content:
                # If no tag was found for this chunk, it's "normal"
                current_tag = tag.lower() if tag else "normal"
                parts.append((current_tag, content))
        
        return parts if parts else [("normal", text.strip())]

    def generate_audio(self, text, gender="female", filepath="output.wav"):
        voice = self.voices.get(gender.lower(), "af_bella")
        parts = self.parse_text(text)
        final_audio = AudioSegment.empty()

        for tag, sentence in parts:
            pitch, speed, is_whisper = 0, 1.0, False
            volume_adj = 0 

            # Emotion Logic
            if tag == "sarcastically":
                pitch, speed = -1.5, 0.8  
            elif tag == "whispers":
                is_whisper = True
                speed, volume_adj = 0.85, -12 
            elif tag == "giggles":
                # Special handling for giggles using phonemes
                generator = self.pipeline("ha ha ha", voice=voice)
                for _, _, audio in generator:
                    audio = self.apply_dsp(audio, pitch=3, speed=1.6)
                    seg = self.to_segment(audio).fade_out(100)
                    final_audio += seg[:400]
                # After giggling, we still speak the text associated with the tag if any
                if not sentence or sentence.lower() in ["ha", "haha", "giggles"]:
                    continue

            # Generate the actual speech
            generator = self.pipeline(sentence, voice=voice)
            for _, _, audio in generator:
                audio = self.apply_dsp(audio, pitch, speed, is_whisper)
                segment = self.to_segment(audio) + volume_adj
                
                # Use a small crossfade to keep the voice transitions natural
                if len(final_audio) > 0:
                    final_audio = final_audio.append(segment, crossfade=50)
                else:
                    final_audio += segment

        final_audio.export(filepath, format="wav")
        print(f"Saved: {filepath}")
        return filepath

# -----------------------------
# TEST CASES
# -----------------------------
if __name__ == "__main__":
    engine = TTSEngine()

    # Test 1: Pure Normal Voice (No tags)
    engine.generate_audio(
        "This is a perfectly normal sentence with no emotions.",
        gender="female",
        filepath="normal_only.wav"
    )

    # Test 2: Mixed Emotions
    engine.generate_audio(
        "I am so happy for you [sarcastically], please don't tell anyone [whispers], ha ha [giggles]",
        gender="male",
        filepath="mixed_emotions.wav"
    )