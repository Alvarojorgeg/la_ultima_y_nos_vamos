import uuid
import datetime

class Encuesta:
    def __init__(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.duracion = datetime.timedelta(seconds=duracion_segundos)
        self.creacion = datetime.datetime.now()
        self.timestamp_inicio = self.creacion
        self.votos = {}  # username -> lista de opciones
        self.cerrada = False
        self.tipo = tipo  # "simple" o "multiple"

    def esta_activa(self):
        return not self.cerrada and datetime.datetime.now() < self.creacion + self.duracion

    def cerrar(self):
        self.cerrada = True

    def agregar_voto(self, username, opciones):
        if not self.esta_activa():
            raise Exception("Encuesta cerrada")
        if isinstance(opciones, str):
            opciones = [opciones]
        self.votos[username] = opciones

    def contar_votos(self):
        conteo = {op: 0 for op in self.opciones}
        for opciones_usuario in self.votos.values():
            for op in opciones_usuario:
                if op in conteo:
                    conteo[op] += 1
        return conteo

    def total_votos(self):
        return sum(len(v) for v in self.votos.values())

    @property
    def estado(self):
        if self.cerrada:
            return "cerrada"
        elif self.esta_activa():
            return "activa"
        else:
            return "expirada"

    def to_dict(self):
        return {
            "id": self.id,
            "pregunta": self.pregunta,
            "opciones": self.opciones,
            "duracion": int(self.duracion.total_seconds()),  # 💡 CONVERTIDO A INT
            "creacion": self.creacion.isoformat(),
            "timestamp_inicio": self.timestamp_inicio.isoformat(),
            "votos": self.votos,
            "cerrada": self.cerrada,
            "tipo": self.tipo
        }

    @classmethod
    def from_dict(cls, d):
        encuesta = cls(
            d.get("pregunta", ""),
            d.get("opciones", []),
            int(d.get("duracion", 60)),
            d.get("tipo", "simple")
        )
        encuesta.id = d.get("id", str(uuid.uuid4()))
        try:
            encuesta.creacion = datetime.datetime.fromisoformat(d["creacion"])
        except KeyError:
            encuesta.creacion = datetime.datetime.now()

        try:
            encuesta.timestamp_inicio = datetime.datetime.fromisoformat(d["timestamp_inicio"])
        except KeyError:
            encuesta.timestamp_inicio = encuesta.creacion

        encuesta.votos = d.get("votos", {})
        encuesta.cerrada = d.get("cerrada", False)
        return encuesta
