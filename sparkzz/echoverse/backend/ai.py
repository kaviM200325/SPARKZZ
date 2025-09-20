import os
from gtts import gTTS

# Voice mapping for gTTS accents via TLD (top-level domain)
# gTTS accent variants are controlled by the 'tld' parameter, not the lang code.
VOICE_TLD = {
    'allison': 'com',      # US
    'michael': 'co.uk',    # UK
    'lisa': 'com.au'       # AU
}


def transcribe_audio(audio_path: str) -> str:
    """Mock transcribe audio for demonstration."""
    return "This is a mock transcription of the uploaded audio file."


def rewrite_text_tone(text: str, tone: str = 'Neutral') -> str:
    """Mock rewrite text in a chosen tone for demonstration."""
    if tone == 'Neutral':
        return text
    elif tone == 'Suspenseful':
        return f"In a heart-pounding moment, {text.lower()}"
    elif tone == 'Inspiring':
        return f"In an uplifting way, {text.lower()}"
    else:
        return text


def generate_audio_from_text(text: str, voice_key: str, filename: str) -> str:
    """
    Generate audio using gTTS and save as MP3 (no heavy audio libraries).
    Streamlit can play MP3 directly.
    """
    # Ensure MP3 extension
    if not filename.lower().endswith('.mp3'):
        filename = f"{filename}.mp3"

    tld = VOICE_TLD.get(voice_key, 'com')

    # Create output directory if needed
    out_dir = os.path.dirname(filename)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Synthesize speech
    tts = gTTS(text=text, lang='en', tld=tld)
    # Overwrite if exists
    if os.path.exists(filename):
        os.remove(filename)
    tts.save(filename)

    return filename
