# src/patterns/observer.py

from abc import ABC, abstractmethod
from src.models.encuesta import Encuesta

# Interfaz del Observador
class ObservadorCierreEncuesta(ABC):
    @abstractmethod
    def update(self, encuesta: Encuesta):
        pass

# Sujeto (ya está integrado en PollService)
# Los observadores se registran con .registrar_observador()
