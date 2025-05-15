# src/models/encuesta.py

import uuid
from datetime import datetime, timedelta
from typing import List, Dict


class Encuesta:
    def __init__(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple"):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.tipo = tipo  # "simple", "multiple", "ponderada", etc.
        self.votos: Dict[str, List[str]] = {}  # username -> [opciones]
        self.estado = "activa"
        self.timestamp_inicio = datetime.utcnow()
        self.duracion = timedelta(seconds=duracion_segundos)
        self.timestamp_cierre = self.timestamp_inicio + self.duracion

    def esta_activa(self) -> bool:
        return self.estado == "activa" and datetime.utcnow() < self.timestamp_cierre

    def cerrar(self):
        self.estado = "cerrada"

    def agregar_voto(self, username: str, opciones_votadas: List[str]):
        if username in self.votos:
            raise ValueError("El usuario ya ha votado en esta encuesta.")
        if not self.esta_activa():
            raise ValueError("La encuesta ya está cerrada.")
        if self.tipo == "simple" and len(opciones_votadas) != 1:
            raise ValueError("Esta encuesta solo permite una opción por voto.")
        self.votos[username] = opciones_votadas

    def resultados(self) -> Dict[str, int]:
        conteo = {opcion: 0 for opcion in self.opciones}
        for opciones_usuario in self.votos.values():
            for opcion in opciones_usuario:
                if opcion in conteo:
                    conteo[opcion] += 1
        return conteo

    def total_votos(self) -> int:
        return sum(len(opciones) for opciones in self.votos.values())
