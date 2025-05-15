# src/patterns/factory.py

from abc import ABC, abstractmethod
from src.models.encuesta import Encuesta


class EncuestaFactory(ABC):
    @abstractmethod
    def crear_encuesta(self, pregunta: str, opciones: list, duracion_segundos: int) -> Encuesta:
        pass


class EncuestaSimpleFactory(EncuestaFactory):
    def crear_encuesta(self, pregunta: str, opciones: list, duracion_segundos: int) -> Encuesta:
        return Encuesta(pregunta, opciones, duracion_segundos, tipo="simple")


class EncuestaMultipleFactory(EncuestaFactory):
    def crear_encuesta(self, pregunta: str, opciones: list, duracion_segundos: int) -> Encuesta:
        return Encuesta(pregunta, opciones, duracion_segundos, tipo="multiple")


class EncuestaFactorySelector:
    @staticmethod
    def get_factory(tipo: str) -> EncuestaFactory:
        if tipo == "multiple":
            return EncuestaMultipleFactory()
        else:
            return EncuestaSimpleFactory()
