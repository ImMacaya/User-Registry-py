from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    password_salt: str
    is_active: bool
    created_at: str
    updated_at: str

    @staticmethod
    def now_iso() -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )
