import gradio as gr
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.nft_repo import NFTRepository
from src.repositories.usuario_repo import UsuarioRepository

# Instanciar repositorios
encuesta_repo = EncuestaRepository()
nft_repo = NFTRepository()
user_repo = UsuarioRepository()

# Instanciar servicios
nft_service = NFTService(nft_repo, user_repo)
poll_service = PollService(encuesta_repo, nft_service)

# Funciones para la interfaz Gradio
def crear_encuesta(pregunta, opciones, duracion):
    opciones_list = [op.strip() for op in opciones.split(",")]
    encuesta = poll_service.crear_encuesta(pregunta, opciones_list, int(duracion))
    return f"Encuesta creada con ID: {encuesta.id}"

def votar(poll_id, username, opcion):
    try:
        poll_service.votar(poll_id, username, [opcion])
        return "Voto registrado correctamente"
    except Exception as e:
        return f"Error: {str(e)}"

# Interfaz con Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Crear Encuesta")
    pregunta = gr.Textbox(label="Pregunta")
    opciones = gr.Textbox(label="Opciones (separadas por coma)")
    duracion = gr.Number(label="Duración (segundos)", value=60)
    crear_btn = gr.Button("Crear encuesta")
    crear_output = gr.Textbox(label="Resultado")
    crear_btn.click(fn=crear_encuesta, inputs=[pregunta, opciones, duracion], outputs=crear_output)

    gr.Markdown("## Votar en Encuesta")
    poll_id = gr.Textbox(label="ID de la encuesta")
    username = gr.Textbox(label="Usuario")
    opcion = gr.Textbox(label="Opción")
    votar_btn = gr.Button("Votar")
    votar_output = gr.Textbox(label="Resultado")
    votar_btn.click(fn=votar, inputs=[poll_id, username, opcion], outputs=votar_output)

# Lanzar app
if __name__ == "__main__":
    demo.launch()
