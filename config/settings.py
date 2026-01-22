import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)
