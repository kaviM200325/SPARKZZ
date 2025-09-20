import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = BASE_DIR / 'examples'
EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_text(uploaded_file) -> str:
    dest = BASE_DIR / 'uploads'
    dest.mkdir(parents=True, exist_ok=True)
    filepath = dest / uploaded_file.name
    with open(filepath, 'wb') as f:
        f.write(uploaded_file.getvalue())
    return str(filepath)

def list_sample_files():
    return [f.name for f in EXAMPLES_DIR.glob('*.txt')]

def read_text_file(path: str) -> str:
    p = Path(path)
    # Resolve relative paths against the project base directory to ensure
    # consistent behavior regardless of current working directory.
    if not p.is_absolute():
        p = BASE_DIR / p
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()
