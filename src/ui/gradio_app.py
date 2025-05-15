# src/ui/gradio_app.py

import gradio as gr
from src.services.poll_service import PollService
from src.services.chatbot_service import ChatbotService
from src.services.nft_service import NFTService


class UIController:
    def __init__(self, poll_service: PollService, chatbot_service: ChatbotService, nft_service: NFTService):
        self.poll_service = poll_service
        self.chatbot_service = chatbot_service
        self.nft_service = nft_service

    def interfaz(self):
        with gr.Blocks() as demo:
            gr.Markdown("# 🎥 Encuestas Interactivas del Stream")

            with gr.Tab("📊 Votación"):
                encuesta_id_input = gr.Text(label="ID de la encuesta")
                username_input = gr.Text(label="Tu nombre de usuario")
                opcion_input = gr.Text(label="Opción a votar (texto exacto)")
                votar_btn = gr.Button("Votar")
                voto_output = gr.Textbox(label="Resultado del voto")

                def votar_web(poll_id, username, opcion):
                    try:
                        self.poll_service.votar(poll_id, username, [opcion])
                        return "✅ Voto registrado"
                    except Exception as e:
                        return f"❌ {str(e)}"

                votar_btn.click(votar_web, inputs=[encuesta_id_input, username_input, opcion_input], outputs=voto_output)

            with gr.Tab("🤖 Chatbot"):
                chat = gr.ChatInterface(fn=self.chatbot_service.responder)

            with gr.Tab("🎟️ Mis Tokens"):
                user_token_input = gr.Text(label="Tu usuario")
                mostrar_btn = gr.Button("Mostrar mis tokens")
                tokens_output = gr.Textbox(label="Tokens")

                def ver_tokens(username):
                    tokens = self.nft_service.obtener_tokens_usuario(username)
                    if not tokens:
                        return "📭 No tienes tokens"
                    return "\n".join([f"{t.token_id}: {t.option} ({t.poll_id})" for t in tokens])

                mostrar_btn.click(ver_tokens, inputs=[user_token_input], outputs=tokens_output)

        return demo
