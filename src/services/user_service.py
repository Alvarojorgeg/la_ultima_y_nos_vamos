# src/services/user_service.py

import uuid
from typing import Optional
from src.models.usuario import Usuario
from src.repositories.usuario_repo import UsuarioRepository


class UserService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
        self.sesiones = {}  # session_token -> username

    def registrar(self, username: str, password: str) -> Usuario:
        if self.repo.obtener_por_username(username):
            raise ValueError("El nombre de usuario ya está en uso.")

        usuario = Usuario(username, password)
        self.repo.guardar(usuario)
        return usuario

    def login(self, username: str, password: str) -> str:
        usuario = self.repo.obtener_por_username(username)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if not usuario.verificar_password(password):
            raise ValueError("Contraseña incorrecta.")

        token_sesion = str(uuid.uuid4())
        self.sesiones[token_sesion] = username
        return token_sesion

    def obtener_usuario_por_token(self, token_sesion: str) -> Optional[Usuario]:
        username = self.sesiones.get(token_sesion)
        if not username:
            return None
        return self.repo.obtener_por_username(username)

    def esta_autenticado(self, token_sesion: str) -> bool:
        return token_sesion in self.sesiones
