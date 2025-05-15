# src/repositories/encuesta_repo.py

import json
import os
from typing import List, Optional
from src.models.encuesta import Encuesta

RUTA_DATOS = "la_ultima_y_nos_vamos/data/encuestas.json"

class EncuestaRepository:
    def __init__(self, ruta_archivo: str = RUTA_DATOS):
        self.ruta_archivo = ruta_archivo
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w") as f:
                json.dump([], f)

    def guardar(self, encuesta: Encuesta):
        encuestas = self.listar_todas()
        encuestas = [e for e in encuestas if e.id != encuesta.id]
        encuestas.append(encuesta)
        with open(self.ruta_archivo, "w") as f:
            json.dump([self._to_dict(e) for e in encuestas], f, indent=2)

    def obtener_por_id(self, poll_id: str) -> Optional[Encuesta]:
        for e in self.listar_todas():
            if e.id == poll_id:
                return e
        return None

    def listar_todas(self) -> List[Encuesta]:
        with open(self.ruta_archivo, "r") as f:
            try:
                datos = json.load(f)
            except json.JSONDecodeError:
                datos = []
        return [self._from_dict(d) for d in datos]

    def _to_dict(self, encuesta: Encuesta) -> dict:
        return {
            "id": encuesta.id,
            "pregunta": encuesta.pregunta,
            "opciones": encuesta.opciones,
            "tipo": encuesta.tipo,
            "votos": encuesta.votos,
            "timestamp_inicio": encuesta.timestamp_inicio.isoformat(),
            "duracion": encuesta.duracion.total_seconds()
        }

    def _from_dict(self, data: dict) -> Encuesta:
        from datetime import datetime, timedelta
        encuesta = Encuesta(
            pregunta=data["pregunta"],
            opciones=data["opciones"],
            duracion_segundos=int(data["duracion"]),
            tipo=data.get("tipo", "simple")
        )
        encuesta.id = data["id"]
        encuesta.votos = data.get("votos", {})
        encuesta.timestamp_inicio = datetime.fromisoformat(data["timestamp_inicio"])
        encuesta.creacion = encuesta.timestamp_inicio
        return encuesta
