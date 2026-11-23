from abc import ABC, abstractmethod

from user_registry.domain.models import User


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def list_all(self) -> list[User]: ...

    @abstractmethod
    def update_name(self, email: str, new_name: str) -> None: ...

    @abstractmethod
    def set_active(self, email: str, is_active: bool) -> None: ...
