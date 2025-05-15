# src/services/nft_service.py

from typing import List
from src.models.token_nft import TokenNFT
from src.repositories.nft_repo import NFTRepository
from src.repositories.usuario_repo import UsuarioRepository


class NFTService:
    def __init__(self, nft_repo: NFTRepository, user_repo: UsuarioRepository):
        self.nft_repo = nft_repo
        self.user_repo = user_repo

    def mint_token(self, owner: str, poll_id: str, option: str) -> TokenNFT:
        token = TokenNFT(owner, poll_id, option)
        self.nft_repo.guardar(token)

        usuario = self.user_repo.obtener_por_username(owner)
        if usuario:
            usuario.agregar_token(token.token_id)
            self.user_repo.guardar(usuario)

        return token

    def transferir_token(self, token_id: str, actual_owner: str, nuevo_owner: str) -> bool:
        token = self.nft_repo.obtener_por_id(token_id)
        if not token or token.owner != actual_owner:
            return False

        # Transferencia lógica
        token.transferir(nuevo_owner)
        self.nft_repo.guardar(token)

        # Actualizar usuarios
        usuario_actual = self.user_repo.obtener_por_username(actual_owner)
        usuario_nuevo = self.user_repo.obtener_por_username(nuevo_owner)
        if not usuario_actual or not usuario_nuevo:
            return False

        usuario_actual.eliminar_token(token_id)
        usuario_nuevo.agregar_token(token_id)

        self.user_repo.guardar(usuario_actual)
        self.user_repo.guardar(usuario_nuevo)
        return True

    def obtener_tokens_usuario(self, username: str) -> List[TokenNFT]:
        return self.nft_repo.obtener_por_owner(username)
