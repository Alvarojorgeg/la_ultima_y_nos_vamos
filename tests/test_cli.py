
# tests/test_cli.py

import pytest
from src.controllers.cli_controller import CLIController
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.nft_repo import NFTRepository
import tempfile
import builtins


@pytest.fixture
def controlador():
    with tempfile.NamedTemporaryFile(delete=False) as tf1, tempfile.NamedTemporaryFile(delete=False) as tf2, tempfile.NamedTemporaryFile(delete=False) as tf3:
        encuesta_repo = EncuestaRepository(tf1.name)
        usuario_repo = UsuarioRepository(tf2.name)
        nft_repo = NFTRepository(tf3.name)

        user_service = UserService(usuario_repo)
        user_service.registrar("cliuser", "pass")
        nft_service = NFTService(nft_repo, usuario_repo)
        poll_service = PollService(encuesta_repo, nft_service)

        return CLIController(poll_service, user_service, nft_service)


def test_procesar_comando_desconocido(controlador, capsys):
    controlador.procesar_comando("comando_que_no_existe")
    salida = capsys.readouterr().out
    assert "no reconocido" in salida


def test_ayuda_muestra_comandos(controlador, capsys):
    controlador.procesar_comando("ayuda")
    salida = capsys.readouterr().out
    assert "registrar" in salida
    assert "crear_encuesta" in salida
