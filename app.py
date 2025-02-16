import gradio as gr
from agent import run_conversation

def gradio_interface(user_prompt):
    return run_conversation(user_prompt)  

interface = gr.Interface(fn=gradio_interface, inputs="text", outputs="text")
interface.launch()