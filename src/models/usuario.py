# src/models/usuario.py
import bcrypt
from typing import List


class Usuario:
    def __init__(self, username: str, password_plano: str, tokens: List[str] = None):
        self.username = username
        self.password_hash = self._hashear_password(password_plano)
        self.tokens = tokens or []  # Lista de IDs de tokens NFT

    def _hashear_password(self, password_plano: str) -> str:
        return bcrypt.hashpw(password_plano.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_password(self, password_plano: str) -> bool:
        return bcrypt.checkpw(password_plano.encode('utf-8'), self.password_hash.encode('utf-8'))

    def agregar_token(self, token_id: str):
        if token_id not in self.tokens:
            self.tokens.append(token_id)

    def eliminar_token(self, token_id: str):
        if token_id in self.tokens:
            self.tokens.remove(token_id)

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "tokens": self.tokens
        }

    @staticmethod
    def from_dict(data: dict):
        usuario = Usuario.__new__(Usuario)
        usuario.username = data["username"]
        usuario.password_hash = data["password_hash"]
        usuario.tokens = data.get("tokens", [])
        return usuario