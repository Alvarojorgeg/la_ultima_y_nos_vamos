# src/patterns/strategy.py

from abc import ABC, abstractmethod
import random
from typing import List, Dict


class DesempateStrategy(ABC):
    @abstractmethod
    def resolver(self, opciones_empate: List[str]) -> str:
        pass


class DesempateAlfabetico(DesempateStrategy):
    def resolver(self, opciones_empate: List[str]) -> str:
        return sorted(opciones_empate)[0]


class DesempateAleatorio(DesempateStrategy):
    def resolver(self, opciones_empate: List[str]) -> str:
        return random.choice(opciones_empate)


class DesempateProrroga(DesempateStrategy):
    def resolver(self, opciones_empate: List[str]) -> str:
        # En este ejemplo, simplemente devuelve un aviso
        return "empate - se requiere prórroga"

        
class StrategySelector:
    @staticmethod
    def get_strategy(nombre: str) -> DesempateStrategy:
        if nombre == "aleatorio":
            return DesempateAleatorio()
        elif nombre == "prorroga":
            return DesempateProrroga()
        else:
            return DesempateAlfabetico()
