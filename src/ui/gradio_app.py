import gradio as gr
import datetime
from src.repositories.encuesta_repo import EncuestaRepository
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.repositories.nft_repo import NFTRepository
from src.repositories.usuario_repo import UsuarioRepository
from src.models.encuesta import Encuesta

# Repositorios y servicios
encuesta_repo = EncuestaRepository()
nft_repo = NFTRepository()
usuario_repo = UsuarioRepository()
nft_service = NFTService(nft_repo, usuario_repo)
poll_service = PollService(encuesta_repo, nft_service)

# Chatbot

def chatbot_interface(message, history):
    message = message.lower()
    if "crear encuesta" in message:
        return "Puedes usar la sección de 'Crear Encuesta' abajo."
    elif "votar" in message:
        return "Ve a la sección 'Votar Encuesta'."
    elif "resultados" in message:
        return "(Próximamente) Podrás ver los resultados."
    elif "nft" in message:
        return "Los NFTs se generan al votar."
    else:
        return "Hola! Puedes decir cosas como: 'crear encuesta', 'votar', 'ver resultados', 'nft'."

# Funciones de encuesta

def crear_encuesta(pregunta, opciones, duracion):
    opciones_list = [o.strip() for o in opciones.split(",") if o.strip()]
    try:
        encuesta = poll_service.crear_encuesta(pregunta, opciones_list, int(duracion))
        return f"Encuesta creada con ID: {encuesta.id}"
    except Exception as e:
        return f"Error: {str(e)}"

def votar_encuesta(encuesta_id, username, opcion):
    try:
        poll_service.votar(encuesta_id, username, [opcion])
        return f"Voto registrado para {username}."
    except Exception as e:
        return f"Error al votar: {str(e)}"

# Componentes Gradio
chatbot = gr.ChatInterface(chatbot_interface, title="Asistente Encuestas NFT")

crear_encuesta_inputs = [
    gr.Textbox(label="Pregunta"),
    gr.Textbox(label="Opciones (separadas por coma)"),
    gr.Number(label="Duración en segundos")
]
crear_encuesta_btn = gr.Button("Crear Encuesta")
crear_encuesta_output = gr.Textbox(label="Resultado")

votar_inputs = [
    gr.Textbox(label="ID Encuesta"),
    gr.Textbox(label="Usuario"),
    gr.Textbox(label="Opción a votar")
]
votar_btn = gr.Button("Votar")
votar_output = gr.Textbox(label="Resultado voto")

# Layout completo
with gr.Blocks(title="Encuestas + Chatbot + NFT") as app:
    gr.Markdown("# Plataforma Encuestas con NFT y Asistente Virtual")

    with gr.Tab("Asistente"):
        chatbot.render()

    with gr.Tab("Crear Encuesta"):
        gr.Markdown("## Crear una nueva encuesta")
        with gr.Row():
            for comp in crear_encuesta_inputs:
                comp.render()
        crear_encuesta_btn.render()
        crear_encuesta_output.render()
        crear_encuesta_btn.click(fn=crear_encuesta, inputs=crear_encuesta_inputs, outputs=crear_encuesta_output)

    with gr.Tab("Votar Encuesta"):
        gr.Markdown("## Votar en encuesta existente")
        with gr.Row():
            for comp in votar_inputs:
                comp.render()
        votar_btn.render()
        votar_output.render()
        votar_btn.click(fn=votar_encuesta, inputs=votar_inputs, outputs=votar_output)

if __name__ == "__main__":
    app.launch()
