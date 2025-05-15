
# tests/test_patterns.py

from src.models.encuesta import Encuesta
from src.patterns.factory import EncuestaFactorySelector
from src.patterns.strategy import StrategySelector
from src.patterns.observer import ObservadorCierreEncuesta


def test_factory_selector():
    factory = EncuestaFactorySelector.get_factory("multiple")
    encuesta = factory.crear_encuesta("¿Lenguaje?", ["Python", "Java"], 30)
    assert encuesta.tipo == "multiple"

    factory2 = EncuestaFactorySelector.get_factory("simple")
    encuesta2 = factory2.crear_encuesta("¿Café o té?", ["Café", "Té"], 30)
    assert encuesta2.tipo == "simple"


def test_strategy_resolver():
    opciones = ["A", "B"]
    estrategia_abc = StrategySelector.get_strategy("alfabetico")
    resultado = estrategia_abc.resolver(opciones)
    assert resultado == "A"

    estrategia_rand = StrategySelector.get_strategy("aleatorio")
    resultado2 = estrategia_rand.resolver(opciones)
    assert resultado2 in opciones


def test_observer_recibe_update():
    clase_llamada = {"notificado": False}

    class ObservadorPrueba(ObservadorCierreEncuesta):
        def update(self, encuesta):
            clase_llamada["notificado"] = True

    encuesta = Encuesta("¿Test?", ["Sí", "No"], 10)
    from src.services.poll_service import PollService
    from src.services.nft_service import NFTService
    from src.repositories.encuesta_repo import EncuestaRepository
    from src.repositories.nft_repo import NFTRepository
    from src.repositories.usuario_repo import UsuarioRepository
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False) as efile, tempfile.NamedTemporaryFile(delete=False) as tfile, tempfile.NamedTemporaryFile(delete=False) as ufile:
        poll_service = PollService(EncuestaRepository(ruta_archivo=efile.name), NFTService(NFTRepository(tfile.name), UsuarioRepository(ufile.name)))
        observador = ObservadorPrueba()
        poll_service.registrar_observador(observador)
        encuesta.cerrar()
        poll_service.notificar_cierre(encuesta)

        assert clase_llamada["notificado"]

    import os
    os.remove(efile.name)
    os.remove(tfile.name)
    os.remove(ufile.name)
