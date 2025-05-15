# src/services/chatbot_service.py

from transformers import pipeline, Conversation
from src.services.poll_service import PollService


class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")
        self.poll_service = poll_service

    def responder(self, username: str, mensaje: str) -> str:
        mensaje = mensaje.lower()

        # Preguntas sobre encuestas activas
        if "quién va ganando" in mensaje or "resultado" in mensaje:
            encuestas = self.poll_service.repo.listar_todas()
            activas = [e for e in encuestas if e.estado == "activa"]
            if not activas:
                return "No hay encuestas activas en este momento."
            respuestas = []
            for e in activas:
                resultados = e.resultados()
                resumen = ", ".join([f"{op}: {res}" for op, res in resultados.items()])
                respuestas.append(f"Encuesta: {e.pregunta} → {resumen}")
            return "\n".join(respuestas)

        if "cuánto falta" in mensaje or "cuándo cierra" in mensaje:
            encuestas = self.poll_service.repo.listar_todas()
            activas = [e for e in encuestas if e.estado == "activa"]
            if not activas:
                return "No hay encuestas activas actualmente."
            mensajes = []
            for e in activas:
                segundos_restantes = int((e.timestamp_cierre - e.timestamp_inicio).total_seconds())
                mensajes.append(f"Encuesta: {e.pregunta} → cierra en aproximadamente {segundos_restantes} segundos.")
            return "\n".join(mensajes)

        # Para todo lo demás: IA
        conv = Conversation(mensaje)
        respuesta = self.chatbot(conv)
        return respuesta.generated_responses[-1]
