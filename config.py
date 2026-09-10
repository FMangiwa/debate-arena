import os
from dotenv import load_dotenv

# Load API Keys
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# API Base URLs compatible with OpenAI SDK
ENDPOINTS = {
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "ollama": "http://localhost:11434/v1"
}

# Model Choices
MODELS = {
    "GPT-5-Mini": {"provider": "OpenAI", "model_id": "gpt-5-mini"},
    "Gemini 3.1 Flash Lite": {"provider": "Gemini", "model_id": "gemini-3.1-flash-lite"},
    "Llama 3.2 (Local Ollama)": {"provider": "Ollama", "model_id": "llama3.2"}
}

# Pre-defined System Personas
DEFAULT_PERSONAS = {
    "Alex (Skeptical & Snarky)": "You are Alex, an argumentative, highly skeptical AI. Challenge assumptions and point out flaws concisely.",
    "Blake (Diplomatic Peacemaker)": "You are Blake, a polite, constructive AI. Seek common ground, validate insights, and keep conversations balanced.",
    "Charlie (Hyper-Logical Analyst)": "You are Charlie, a hyper-logical scientific AI. Base every observation on strict facts, data, and structured analysis."
}