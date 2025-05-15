# tests/test_services.py

import tempfile
from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.nft_repo import NFTRepository
from src.repositories.encuesta_repo import EncuestaRepository

from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.poll_service import PollService


def test_registro_y_login_usuario():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        repo = UsuarioRepository(ruta_archivo=tf.name)
        service = UserService(repo)

        user = service.registrar("juan", "clave123")
        assert user.username == "juan"

        token = service.login("juan", "clave123")
        assert service.esta_autenticado(token)

    repo_path = tf.name
    import os
    os.remove(repo_path)


def test_mint_token_nft():
    with tempfile.NamedTemporaryFile(delete=False) as tf1, tempfile.NamedTemporaryFile(delete=False) as tf2:
        nft_repo = NFTRepository(ruta_archivo=tf1.name)
        user_repo = UsuarioRepository(ruta_archivo=tf2.name)
        user_repo.guardar(UserService(user_repo).registrar("ana", "pass"))

        nft_service = NFTService(nft_repo, user_repo)
        token = nft_service.mint_token("ana", "pollX", "Opción Z")

        tokens = nft_service.obtener_tokens_usuario("ana")
        assert any(t.token_id == token.token_id for t in tokens)

    import os
    os.remove(tf1.name)
    os.remove(tf2.name)


def test_crear_y_votar_encuesta():
    with tempfile.NamedTemporaryFile(delete=False) as tf1, tempfile.NamedTemporaryFile(delete=False) as tf2, tempfile.NamedTemporaryFile(delete=False) as tf3:
        encuesta_repo = EncuestaRepository(ruta_archivo=tf1.name)
        user_repo = UsuarioRepository(ruta_archivo=tf2.name)
        nft_repo = NFTRepository(ruta_archivo=tf3.name)

        user_service = UserService(user_repo)
        user_service.registrar("luis", "clave")
        nft_service = NFTService(nft_repo, user_repo)
        poll_service = PollService(encuesta_repo, nft_service)

        encuesta = poll_service.crear_encuesta("¿A o B?", ["A", "B"], 10)
        poll_service.votar(encuesta.id, "luis", ["A"])
        resultados = poll_service.obtener_resultados_parciales(encuesta.id)

        assert resultados["A"] == 1

    import os
    os.remove(tf1.name)
    os.remove(tf2.name)
    os.remove(tf3.name)
