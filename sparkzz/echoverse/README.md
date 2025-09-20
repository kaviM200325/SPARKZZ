# EchoVerse — AI-Powered Audiobook Creation Tool

This is a complete, professional project for EchoVerse, implemented with Python + Streamlit and integration points for IBM Watson (LLM-like rewrites and Text-to-Speech).

## Quick Setup

### Prerequisites
- Python 3.10+
- pip
- An IBM Cloud account with access to Text-to-Speech and Watsonx/Assistant/LLM services.

### Installation
1. Clone or copy the files into the `echoverse/` directory.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment: `source .venv/bin/activate` (on Windows: `.venv\Scripts\activate`)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your API keys.
6. Run the app: `streamlit run streamlit_app.py`

### Notes
- pydub requires ffmpeg. Install via your package manager if needed (e.g., `apt install ffmpeg` on Ubuntu, `brew install ffmpeg` on macOS, `choco install ffmpeg` on Windows).
- For production, use a secrets manager instead of .env.

## Project Structure
```
echoverse/
├── README.md
├── requirements.txt
├── .env.example
├── run.sh
├── streamlit_app.py
├── backend/
│   ├── __init__.py
│   ├── watson_client.py
│   ├── ai.py
│   └── file_utils.py
├── static/
│   └── styles.css
├── assets/
│   └── logo.png
└── examples/
    └── sample.txt
```

## Additional Notes
- For book-length texts, implement chunking (2-4k chars per chunk) and concatenate MP3s using pydub.
- Add prompt engineering for better rewrites.
- Ensure accessibility with captions and player controls.
- Deploy with Docker for production.
