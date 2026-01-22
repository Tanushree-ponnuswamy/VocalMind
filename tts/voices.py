def get_voice_id_by_gender(engine, gender_input):
    """
    Returns a voice ID for pyttsx3 based on system available voices.
    Attempts to find a Male or Female voice in the installed system voices.
    """
    voices = engine.getProperty('voices')
    
    # Simple heuristic to find male/female voices
    # Note: Accuracy depends on system voice metadata
    target_gender = 'male' if gender_input == '1' else 'female'
    
    for voice in voices:
        # Check if gender metadata exists and matches
        # This varies by OS and installed voices
        if hasattr(voice, 'gender') and voice.gender:
             # Some systems return 'VoiceGender.Male' enum or string
            if str(voice.gender).lower() == target_gender:
                return voice.id
        
        # Fallback: check name for 'David' (Male) or 'Zira' (Female) common on Windows
        name_lower = voice.name.lower()
        if target_gender == 'male' and ('david' in name_lower or 'male' in name_lower):
            return voice.id
        if target_gender == 'female' and ('zira' in name_lower or 'female' in name_lower):
            return voice.id
            
    # If no specific match found, return a fallback based on index if available
    if voices:
        # Usually 0 is Male, 1 is Female on standard Windows SAPI5 (David/Zira)
        if gender_input == '2' and len(voices) > 1:
            return voices[1].id
        return voices[0].id
        
    return None

