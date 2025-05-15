# src/repositories/usuario_repo.py

import json
import os
from typing import Optional, List
from src.models.usuario import Usuario

RUTA_USUARIOS = "la_ultima_y_nos_vamos/data/usuarios.json"


class UsuarioRepository:
    def __init__(self, ruta_archivo: str = RUTA_USUARIOS):
        self.ruta_archivo = ruta_archivo
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w") as f:
                json.dump([], f)

    def guardar(self, usuario: Usuario):
        usuarios = self.listar_todos()
        usuarios = [u for u in usuarios if u.username != usuario.username]
        usuarios.append(usuario)
        with open(self.ruta_archivo, "w") as f:
            json.dump([u.to_dict() for u in usuarios], f, indent=2)

    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        for u in self.listar_todos():
            if u.username == username:
                return u
        return None

    def listar_todos(self):
        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            datos = json.loads(contenido)
            return [Usuario.from_dict(d) for d in datos]
