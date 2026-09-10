import gradio as gr
from engine import run_debate_round

def start_arena(topic, rounds):
    """Generator function that yields streaming updates of the debate transcript."""
    for update in run_debate_round(topic, int(rounds)):
        yield update

def clear_inputs():
    """Returns default blank states to reset the input fields and output transcript."""
    return "", 2, "*Debate transcript will appear here...*"

# Custom CSS targeting all Markdown headings inside styled blocks
custom_css = """
/* Base typography and sizing */
body, .gradio-container, button, input, textarea, label, span {
    font-size: 1.5rem !important;
    line-height: 1.6 !important;
}

textarea, input {
    font-size: 1.2rem !important;
}

#debate-output {
    font-size: 1.5rem !important;
    line-height: 1.7 !important;
    padding: 24px !important;
    background-color: var(--background-fill-secondary) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border-color-primary) !important;
}

/* Default Light Mode Agent Colors */
:root {
    --agent-alex: #059669;    /* Deep Emerald Green */
    --agent-blake: #2563eb;   /* Deep Royal Blue */
    --agent-charlie: #ea580c; /* Deep Warm Orange */
}

/* Automatic Dark Mode Override when user toggles dark theme */
.dark, [data-theme="dark"] {
    --agent-alex: #34d399;    /* Bright Mint Green */
    --agent-blake: #60a5fa;   /* Bright Sky Blue */
    --agent-charlie: #fb923c; /* Bright Amber Orange */
}

/* Apply CSS Variables to Agent Classes */
.agent-alex {
    color: var(--agent-alex) !important;
}
.agent-blake {
    color: var(--agent-blake) !important;
}
.agent-charlie {
    color: var(--agent-charlie) !important;
}

/* Force headings, paragraphs, and lists inside agent blocks to inherit theme color */
.agent-alex *, .agent-blake *, .agent-charlie * {
    color: inherit !important;
}
"""

with gr.Blocks(title="Multi-LLM Debate Arena", css=custom_css) as demo:
    gr.Markdown("# 🤖 Multi-LLM Debate Arena & Persona Orchestrator")
    gr.Markdown("Watch multiple LLM providers debate complex topics using custom system prompts in real-time.")
    
    with gr.Row():
        topic_input = gr.Textbox(
            label="Debate Topic / Question", 
            placeholder="Should AI models be open-sourced or kept behind cloud APIs?", 
            lines=2
        )
        rounds_slider = gr.Slider(minimum=1, maximum=5, value=2, step=1, label="Debate Rounds")
    
    with gr.Row():
        start_btn = gr.Button("🚀 Launch Debate", variant="primary")
        stop_btn = gr.Button("🛑 Stop Debate", variant="stop")
        reset_btn = gr.Button("🔄 Reset Arena", variant="secondary")
        
    debate_output = gr.Markdown(
        label="Live Debate Transcript", 
        value="*Debate transcript will appear here...*",
        elem_id="debate-output"
    )
    
    debate_event = start_btn.click(
        fn=start_arena,
        inputs=[topic_input, rounds_slider],
        outputs=[debate_output]
    )
    
    stop_btn.click(
        fn=lambda: None,
        inputs=None,
        outputs=None,
        cancels=[debate_event]
    )
    
    reset_btn.click(
        fn=clear_inputs,
        inputs=None,
        outputs=[topic_input, rounds_slider, debate_output],
        cancels=[debate_event]
    )

if __name__ == "__main__":
    demo.launch(inbrowser=True, share=False)