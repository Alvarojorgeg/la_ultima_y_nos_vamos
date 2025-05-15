# src/services/poll_service.py

from typing import List
from datetime import datetime
from src.models.encuesta import Encuesta
from src.repositories.encuesta_repo import EncuestaRepository
from src.services.nft_service import NFTService


class PollService:
    def __init__(self, repo: EncuestaRepository, nft_service: NFTService):
        self.repo = repo
        self.nft_service = nft_service
        self.observadores = []

    def registrar_observador(self, obs):
        self.observadores.append(obs)

    def notificar_cierre(self, encuesta: Encuesta):
        for obs in self.observadores:
            obs.update(encuesta)

    def crear_encuesta(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple") -> Encuesta:
        encuesta = Encuesta(pregunta, opciones, duracion_segundos, tipo)
        self.repo.guardar(encuesta)
        return encuesta

    def votar(self, poll_id: str, username: str, opciones: List[str]):
        encuesta = self.repo.obtener_por_id(poll_id)
        if encuesta is None:
            raise ValueError("Encuesta no encontrada.")

        self._verificar_y_cerrar_si_expirada(encuesta)

        encuesta.agregar_voto(username, opciones)
        self.repo.guardar(encuesta)

        # Emitir token NFT
        for opcion in opciones:
            self.nft_service.mint_token(username, encuesta.id, opcion)

    def cerrar_encuesta(self, poll_id: str):
        encuesta = self.repo.obtener_por_id(poll_id)
        if encuesta is None:
            raise ValueError("Encuesta no encontrada.")

        encuesta.cerrar()
        self.repo.guardar(encuesta)
        self.notificar_cierre(encuesta)

    def obtener_resultados_parciales(self, poll_id: str) -> dict:
        encuesta = self.repo.obtener_por_id(poll_id)
        if encuesta is None:
            raise ValueError("Encuesta no encontrada.")

        return encuesta.resultados()

    def obtener_resultados_finales(self, poll_id: str) -> dict:
        encuesta = self.repo.obtener_por_id(poll_id)
        if encuesta is None or encuesta.estado != "cerrada":
            raise ValueError("Encuesta no encontrada o aún activa.")

        resultados = encuesta.resultados()

        # Aquí podrías llamar a la Strategy de desempate si es necesario
        return resultados

    def _verificar_y_cerrar_si_expirada(self, encuesta: Encuesta):
        if encuesta.estado == "activa" and not encuesta.esta_activa():
            self.cerrar_encuesta(encuesta.id)
