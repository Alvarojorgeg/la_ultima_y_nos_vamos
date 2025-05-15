from datetime import datetime

class Encuesta:
    def __init__(self, id, pregunta, opciones, votos=None, estado="activa", timestamp_inicio=None, duracion=60, tipo="unica"):
        self.id = id
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = votos or {}
        self.estado = estado
        self.timestamp_inicio = timestamp_inicio or datetime.now()
        self.duracion = duracion
        self.tipo = tipo

    def agregar_voto(self, username, opcion):
        if username not in self.votos:
            self.votos[username] = []
        self.votos[username].append(opcion)

    def cerrar(self):
        self.estado = "cerrada"

    def esta_activa(self):
        return self.estado == "activa"

    def total_votos(self):
        return sum(len(opciones) for opciones in self.votos.values())

    @staticmethod
    def from_dict(data):
        return Encuesta(
            id=data["id"],
            pregunta=data["pregunta"],
            opciones=data["opciones"],
            votos=data.get("votos", {}),
            estado=data["estado"],
            timestamp_inicio=datetime.fromisoformat(data["timestamp_inicio"]),
            duracion=data["duracion"],
            tipo=data.get("tipo", "unica")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "pregunta": self.pregunta,
            "opciones": self.opciones,
            "votos": self.votos,
            "estado": self.estado,
            "timestamp_inicio": self.timestamp_inicio.isoformat(),
            "duracion": self.duracion,
            "tipo": self.tipo
        }
