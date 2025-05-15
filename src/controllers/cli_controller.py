# src/controllers/cli_controller.py

from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService


class CLIController:
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.sesion_token = None  # Guardará el token de sesión tras login

    def ejecutar(self):
        print("Bienvenido al sistema de votaciones. Escribe 'ayuda' para ver comandos.")
        while True:
            cmd = input("> ").strip()
            if cmd == "salir":
                break
            self.procesar_comando(cmd)

    def procesar_comando(self, cmd: str):
        partes = cmd.split()
        if not partes:
            return

        comando = partes[0]

        if comando == "registrar":
            username = input("Usuario: ")
            password = input("Contraseña: ")
            try:
                self.user_service.registrar(username, password)
                print("✅ Usuario registrado.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

        elif comando == "login":
            username = input("Usuario: ")
            password = input("Contraseña: ")
            try:
                token = self.user_service.login(username, password)
                self.sesion_token = token
                print("🔓 Sesión iniciada.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

        elif comando == "crear_encuesta":
            if not self._requiere_login():
                return
            pregunta = input("Pregunta: ")
            opciones = input("Opciones separadas por coma: ").split(",")
            duracion = int(input("Duración en segundos: "))
            tipo = input("Tipo (simple/multiple): ") or "simple"
            encuesta = self.poll_service.crear_encuesta(pregunta, [o.strip() for o in opciones], duracion, tipo)
            print(f"🆕 Encuesta creada con ID: {encuesta.id}")

        elif comando == "cerrar_encuesta":
            if not self._requiere_login():
                return
            poll_id = input("ID de la encuesta a cerrar: ")
            try:
                self.poll_service.cerrar_encuesta(poll_id)
                print("✅ Encuesta cerrada.")
            except Exception as e:
                print(f"⚠️ Error: {e}")

        elif comando == "ver_resultados":
            poll_id = input("ID de encuesta: ")
            try:
                resultados = self.poll_service.obtener_resultados_parciales(poll_id)
                print("📊 Resultados:")
                for opcion, conteo in resultados.items():
                    print(f"- {opcion}: {conteo} votos")
            except Exception as e:
                print(f"⚠️ Error: {e}")

        elif comando == "mis_tokens":
            if not self._requiere_login():
                return
            user = self.user_service.obtener_usuario_por_token(self.sesion_token)
            tokens = self.nft_service.obtener_tokens_usuario(user.username)
            if tokens:
                print("🎟️ Tus tokens:")
                for t in tokens:
                    print(f"- {t.token_id}: {t.option} ({t.poll_id})")
            else:
                print("📭 No tienes tokens.")

        elif comando == "transferir_token":
            if not self._requiere_login():
                return
            token_id = input("ID del token: ")
            nuevo_owner = input("Nuevo propietario: ")
            user = self.user_service.obtener_usuario_por_token(self.sesion_token)
            ok = self.nft_service.transferir_token(token_id, user.username, nuevo_owner)
            print("✅ Transferido." if ok else "❌ Falló la transferencia.")

        elif comando == "ayuda":
            print("""
Comandos disponibles:
 - registrar
 - login
 - crear_encuesta
 - cerrar_encuesta
 - ver_resultados
 - mis_tokens
 - transferir_token
 - salir
""")
        else:
            print("❓ Comando no reconocido. Escribe 'ayuda'.")

    def _requiere_login(self):
        if not self.sesion_token:
            print("🔒 Debes iniciar sesión primero.")
            return False
        return True
