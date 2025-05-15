# src/app.py

import sys
from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.nft_repo import NFTRepository

from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

from src.controllers.cli_controller import CLIController

def main():
    # Inicialización de repositorios
    encuesta_repo = EncuestaRepository()
    usuario_repo = UsuarioRepository()
    nft_repo = NFTRepository()

    # Servicios
    user_service = UserService(usuario_repo)
    nft_service = NFTService(nft_repo, usuario_repo)
    poll_service = PollService(encuesta_repo, nft_service)
    chatbot_service = ChatbotService(poll_service)

    # CLI por defecto
    if "--ui" in sys.argv:
        print("⚠️ Interfaz Gradio aún no implementada. Ejecutando CLI por defecto.")
    controller = CLIController(poll_service, user_service, nft_service)
    controller.ejecutar()


if __name__ == "__main__":
    main()
