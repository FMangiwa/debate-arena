# 🤖 Multi-LLM Debate Arena & Persona Orchestrator

An interactive multi-agent chat interface built with **Gradio**, **LiteLLM / OpenAI SDK**, and **Python**. The application orchestrates real-time, round-robin debates between multiple frontier and open-weight Large Language Models (LLMs)—such as OpenAI GPT-4.1, Google Gemini, and locally hosted Ollama models—using custom personas.

---

## Demo

This project demonstrates a multi-LLM debate and persona orchestration workflow:

- Supports multiple LLM providers through a unified interface
- Assigns different personas to participating models
- Orchestrates multi-round debate and reasoning
- Streams model responses in real time
- Provides an interactive Gradio interface

---

## ✨ Features

- **Multi-Model Orchestration:** Stream responses sequentially from multiple LLM providers (OpenAI, Gemini via Google AI, Groq, OpenRouter, and local Ollama instances).
- **Custom Agent Personas:** Configurable system prompts assigned to different debaters (e.g., Skeptical Analyst, Diplomatic Peacemaker, Hyper-Logical Engineer).
- **Real-Time Token Streaming:** Live markdown debate updates streamed via Python generators directly to the Gradio UI.
- **Adaptive Dark / Light Theme Styling:** Dynamic CSS color palettes (WCAG compliant) that auto-adjust for high contrast regardless of browser theme mode.
- **Local LLM Output Sanitization:** Automated regex cleaning pipeline to strip extra headers, unwanted self-referential prefixes, and unnecessary markdown meta-labels common in local models (e.g., Llama 3.2 via Ollama).
- **Interactive Controls:** Adjustable debate rounds (1–5), live cancellation (`Stop Debate`), and workspace reset.

---

## 🏗️ Architecture & Project Structure

```text
├── app.py 		# Gradio web interface, custom CSS styling, & event bindings
├── engine.py 		# Core orchestration, stream generator, & regex output sanitization
├── config.py 		# API endpoints, model identifiers, & default persona system prompts
├── requirements.txt 	# Project dependencies
└── Readme.md 		# Documentation

```

---

## ⚙️ Prerequisites

* **Python:** 3.10+ (Python 3.12 recommended)
* **PackageManager:** `uv` or `pip`
* **Optional Local Server:** [Ollama](https://ollama.com/) running locally (e.g., `ollama run llama3.2`) for local model inference.

---

## 🔑 Environment Setup

Create a `.env` file in the root directory and add your API credentials:

```env
# Cloud Model API Keys
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional: Local Ollama Endpoint (Default: http://localhost:11434/v1)
OLLAMA_BASE_URL=http://localhost:11434/v1

```

---

## 🚀 Installation & Running

### Option 1: Using `uv` (Recommended)

```bash
git clone https://github.com/FMangiwa/debate-arena.git
cd debate-arena

# Install dependencies and launch app
uv run python app.py

```

### Option 2: Using standard `pip` and `virtualenv`

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

```

Open your browser at `http://127.0.0.1:7860` to launch the arena.

---

## 🎨 Theme & Color Customization

Debaters are visually distinguished using CSS class variables mapped across both dark and light modes:

| Debater | Model Provider | Light Mode Color | Dark Mode Color |
| --- | --- | --- | --- |
| **Alex** | OpenAI (`GPT-4.1-Mini`) | `#059669` (Deep Emerald) | `#34d399` (Mint Green) |
| **Blake** | Google (`Gemini 3.6 Flash`) | `#2563eb` (Royal Blue) | `#60a5fa` (Sky Blue) |
| **Charlie** | Local (`Llama 3.2 Ollama`) | `#ea580c` (Warm Orange) | `#fb923c` (Vivid Amber) |

---

## License

See `LICENSE`.

---