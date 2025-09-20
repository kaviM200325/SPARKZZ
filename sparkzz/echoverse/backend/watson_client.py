import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Watson / IBM Granite credentials
WATSON_API_KEY = os.getenv("WATSON_API_KEY")
WATSON_URL = os.getenv("WATSON_URL")
GRANITE_MODEL = "ibm-granite/granite-speech-3.3-2b"

# Voice mapping for TTS
VOICE_MAP = {
    'allison': 'en-US_AllisonV3Voice',
    'michael': 'en-US_MichaelV3Voice',
    'lisa': 'en-US_LisaV3Voice'
}

def call_watson_llm(prompt: str) -> str:
    """
    Calls IBM Granite LLM (text generation).
    """
    if not WATSON_API_KEY or not WATSON_URL:
        raise RuntimeError("Missing Watson LLM credentials in .env")

    endpoint = f"{WATSON_URL}/v1/generation"
    headers = {
        "Authorization": f"Bearer {WATSON_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GRANITE_MODEL,
        "input": prompt,
        "parameters": {"decoding_method": "greedy", "max_new_tokens": 200}
    }

    resp = requests.post(endpoint, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()

    return data.get("results", [{}])[0].get("generated_text", "")


def tts_generate_mp3(text: str, voice: str = "en-US_AllisonV3Voice", filename: str = "output.mp3") -> str:
    """
    Calls IBM Watson TTS API to generate speech from text.
    """
    TTS_API_KEY = os.getenv("TTS_API_KEY")
    TTS_URL = os.getenv("TTS_URL")

    if not TTS_API_KEY or not TTS_URL:
        raise RuntimeError("Missing Watson TTS credentials in .env")

    # Map voice if necessary
    voice = VOICE_MAP.get(voice, voice)

    headers = {"Content-Type": "application/json"}
    auth = ("apikey", TTS_API_KEY)

    resp = requests.post(
        f"{TTS_URL}/v1/synthesize",
        headers=headers,
        auth=auth,
        json={"text": text, "voice": voice, "accept": "audio/mp3"}
    )
    resp.raise_for_status()

    with open(filename, "wb") as f:
        f.write(resp.content)

    return filename
