import gradio as gr
from app.api.dtos import ProcessMessageRequestDTO
from app.api.endpoints import process_message

def chat_fn(message, history, user_id):
    req = ProcessMessageRequestDTO(message=message, user_id=user_id)
    print(user_id)
    resp = process_message(req)
    return resp["response"]

user_id_box = gr.Textbox(label="User ID", value="demo-user")

demo = gr.ChatInterface(
    fn=chat_fn,
    additional_inputs=[user_id_box],
    title="Agent Swarm"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)