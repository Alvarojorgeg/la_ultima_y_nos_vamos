
# tests/test_repositories.py

import os
import tempfile
from src.models.usuario import Usuario
from src.models.token_nft import TokenNFT
from src.models.encuesta import Encuesta
from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.nft_repo import NFTRepository
from src.repositories.encuesta_repo import EncuestaRepository


def test_usuario_repo_guardar_y_cargar():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        repo = UsuarioRepository(ruta_archivo=tf.name)
        u = Usuario("testuser", "1234")
        repo.guardar(u)

        u2 = repo.obtener_por_username("testuser")
        assert u2 is not None
        assert u2.username == "testuser"
    os.remove(tf.name)


def test_token_repo_mint_y_busqueda():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        repo = NFTRepository(ruta_archivo=tf.name)
        token = TokenNFT("alice", "poll1", "opcionX")
        repo.guardar(token)

        tokens = repo.obtener_por_owner("alice")
        assert len(tokens) == 1
        assert tokens[0].option == "opcionX"
    os.remove(tf.name)


def test_encuesta_repo_guardar_y_leer():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        repo = EncuestaRepository(ruta_archivo=tf.name)
        e = Encuesta("¿Test?", ["Sí", "No"], 30)
        repo.guardar(e)

        e2 = repo.obtener_por_id(e.id)
        assert e2 is not None
        assert e2.pregunta == "¿Test?"
    os.remove(tf.name)
