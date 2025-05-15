# src/models/voto.py

from typing import List
from datetime import datetime


class Voto:
    def __init__(self, username: str, opciones: List[str], timestamp: datetime = None):
        self.username = username
        self.opciones = opciones
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "opciones": self.opciones,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: dict):
        from datetime import datetime
        return Voto(
            username=data["username"],
            opciones=data["opciones"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
