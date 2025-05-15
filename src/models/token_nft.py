
# src/models/token_nft.py

import uuid
from datetime import datetime


class TokenNFT:
    def __init__(self, owner: str, poll_id: str, option: str, issued_at: datetime = None, token_id: str = None):
        self.token_id = token_id or str(uuid.uuid4())
        self.owner = owner
        self.poll_id = poll_id
        self.option = option
        self.issued_at = issued_at or datetime.utcnow()

    def transferir(self, nuevo_owner: str):
        self.owner = nuevo_owner

    def to_dict(self) -> dict:
        return {
            "token_id": self.token_id,
            "owner": self.owner,
            "poll_id": self.poll_id,
            "option": self.option,
            "issued_at": self.issued_at.isoformat()
        }

    @staticmethod
    def from_dict(data: dict):
        from datetime import datetime
        return TokenNFT(
            owner=data["owner"],
            poll_id=data["poll_id"],
            option=data["option"],
            issued_at=datetime.fromisoformat(data["issued_at"]),
            token_id=data["token_id"]
        )
