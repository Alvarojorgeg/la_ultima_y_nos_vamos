
# tests/test_models.py

from src.models.encuesta import Encuesta
from src.models.voto import Voto
from src.models.usuario import Usuario
from src.models.token_nft import TokenNFT
from datetime import datetime
import uuid


def test_encuesta_basica():
    e = Encuesta("¿Te gusta Python?", ["Sí", "No"], 60)
    assert e.esta_activa()
    e.agregar_voto("alice", ["Sí"])
    assert e.total_votos() == 1
    e.cerrar()
    assert e.estado == "cerrada"


def test_voto_serializacion():
    v = Voto("bob", ["A", "B"])
    d = v.to_dict()
    v2 = Voto.from_dict(d)
    assert v2.username == v.username
    assert v2.opciones == v.opciones


def test_usuario_password():
    u = Usuario("carlos", "secreto123")
    assert u.verificar_password("secreto123")
    assert not u.verificar_password("incorrecto")


def test_token_transferencia():
    token = TokenNFT("alice", "poll123", "Opción A", issued_at=datetime.utcnow(), token_id=str(uuid.uuid4()))
    original_owner = token.owner
    token.transferir("bob")
    assert token.owner != original_owner
