# src/repositories/nft_repo.py

import json
import os
from typing import List, Optional
from src.models.token_nft import TokenNFT

RUTA_TOKENS = "la_ultima_y_nos_vamos/data/tokens.json"


class NFTRepository:
    def __init__(self, ruta_archivo: str = RUTA_TOKENS):
        self.ruta_archivo = ruta_archivo
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w") as f:
                json.dump([], f)

    def guardar(self, token: TokenNFT):
        tokens = self.listar_todos()
        tokens = [t for t in tokens if t.token_id != token.token_id]
        tokens.append(token)
        with open(self.ruta_archivo, "w") as f:
            json.dump([t.to_dict() for t in tokens], f, indent=2)

    def listar_todos(self):
        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            datos = json.loads(contenido)
            return [TokenNFT.from_dict(d) for d in datos]


    def obtener_por_owner(self, owner: str) -> List[TokenNFT]:
        return [t for t in self.listar_todos() if t.owner == owner]

    def obtener_por_id(self, token_id: str) -> Optional[TokenNFT]:
        for t in self.listar_todos():
            if t.token_id == token_id:
                return t
        return None
