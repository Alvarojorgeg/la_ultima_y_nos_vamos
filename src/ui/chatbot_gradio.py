import gradio as gr

def chatbot_interface(message, history):
    message = message.lower()

    if "crear encuesta" in message:
        return "Puedes ir a la sección de 'Crear encuesta' más abajo. Solo llena los campos y pulsa el botón."
    elif "votar" in message:
        return "En la sección 'Votar en encuesta' ingresa el ID, tu nombre de usuario y tu opción."
    elif "ver resultados" in message:
        return "Los resultados aún no se muestran en esta versión, pero puedes agregarlos si quieres subir nota :)"
    elif "nft" in message:
        return "Los NFTs se generan al votar. Puedes ver los tuyos en la sección de NFTs de usuario (si está implementada)."
    else:
        return "Hola! Puedes decir cosas como: 'crear encuesta', 'votar', 'ver resultados' o 'NFT'."

chat = gr.ChatInterface(chatbot_interface, title="Asistente Encuestas NFT")

if __name__ == "__main__":
    chat.launch()
