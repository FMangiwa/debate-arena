import re
from openai import OpenAI
import config

def get_client(provider: str):
    """Factory function to return the correct OpenAI-compatible client."""
    if provider == "OpenAI":
        return OpenAI(api_key=config.OPENAI_API_KEY)
    elif provider == "Gemini":
        return OpenAI(api_key=config.GOOGLE_API_KEY, base_url=config.ENDPOINTS["gemini"])
    elif provider == "Ollama":
        return OpenAI(api_key="ollama", base_url=config.ENDPOINTS["ollama"])
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def clean_agent_output(text: str, agent_name: str) -> str:
    """Strips unnecessary headers, prefixes, and self-referential labels added by Ollama/local models."""
    # Remove markdown headers like ### Observations, ### Rebuttals, ### Response:
    text = re.sub(r"^###?\s*.*?\n", "", text, flags=re.MULTILINE)
    
    # Remove prefixes like "Charlie:", "Charlie (Llama 3.2):", "Response:", "Here is my response:"
    prefix_pattern = rf"^({agent_name}|Response|Here is my response|As an AI|In character)[\w\s\(\)\.\-]*:\s*"
    text = re.sub(prefix_pattern, "", text, flags=re.IGNORECASE).strip()
    
    return text

def stream_agent_response(provider: str, model_id: str, system_prompt: str, agent_name: str, conversation_transcript: str):
    """Streams a response from a selected model while stripping unwanted metadata/prefixes."""
    client = get_client(provider)
    
    # Strict instructions telling the model not to add headers or self-labels
    enhanced_system_prompt = (
        f"{system_prompt}\n\n"
        "STRICT OUTPUT RULES:\n"
        "1. Speak directly in character immediately.\n"
        "2. Do NOT add markdown headings (e.g. do NOT use ###, ##, or headers).\n"
        "3. Do NOT prefix your text with your name, model name, or labels like 'Response:'."
    )
    
    messages = [
        {"role": "system", "content": enhanced_system_prompt},
        {"role": "user", "content": f"Here is the ongoing debate transcript:\n\n{conversation_transcript}\n\nProvide your response (keep it concise, 2-3 sentences):"}
    ]
    
    stream = client.chat.completions.create(
        model=model_id,
        messages=messages,
        stream=True
    )
    
    raw_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        raw_response += delta
        cleaned_response = clean_agent_output(raw_response, agent_name)
        yield cleaned_response

def run_debate_round(topic: str, rounds: int = 2):
    """Executes a round-robin debate generator with dynamic theme-aware styling and clean responses."""
    transcript = f"### Debate Topic: **{topic}**\n\n"
    yield transcript
    
    agent_configs = [
        {
            "name": "Alex",
            "model_key": "GPT-5-Mini",
            "system_prompt": config.DEFAULT_PERSONAS["Alex (Skeptical & Snarky)"],
            "css_class": "agent-alex"
        },
        {
            "name": "Blake",
            "model_key": "Gemini 3.1 Flash Lite",
            "system_prompt": config.DEFAULT_PERSONAS["Blake (Diplomatic Peacemaker)"],
            "css_class": "agent-blake"
        },
        {
            "name": "Charlie",
            "model_key": "Llama 3.2 (Local Ollama)",
            "system_prompt": config.DEFAULT_PERSONAS["Charlie (Hyper-Logical Analyst)"],
            "css_class": "agent-charlie"
        }
    ]
    
    for r in range(rounds):
        transcript += f"---\n#### 🔄 Round {r+1}\n\n"
        for agent in agent_configs:
            model_info = config.MODELS[agent["model_key"]]
            css_class = agent["css_class"]
            
            header = f"<div class='{css_class}' style='margin-bottom: 8px; font-weight: bold;'>{agent['name']} ({agent['model_key']}):</div>\n<div class='{css_class}' style='margin-bottom: 24px;'>"
            
            # Stream cleaned response chunk by chunk
            for partial_response in stream_agent_response(
                model_info["provider"], 
                model_info["model_id"], 
                agent["system_prompt"], 
                agent["name"],
                transcript
            ):
                yield transcript + header + partial_response + "\n</div>"
            
            # Save finished clean turn to transcript
            transcript += header + partial_response + "\n</div>\n\n"