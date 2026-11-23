import pytest

from user_registry.service.user_service import UserService


class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def create(self, user):
        self.users[user.email] = user

    def get_by_email(self, email):
        return self.users.get(email)

    def list_all(self):
        return list(self.users.values())

    def update_name(self, email, new_name):
        self.users[email].name = new_name

    def set_active(self, email, is_active):
        self.users[email].is_active = is_active


def test_create_user_normalizes_email():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    service.create_user(
        name="Macaya",
        email=" MACAYA@EXAMPLE.COM ",
        password="Senha1234",
    )

    # Assert
    assert "macaya@example.com" in repo.users


def test_create_user_rejects_duplicate_email():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Senha1234",
    )

    # Assert
    with pytest.raises(ValueError, match="Já existe"):
        service.create_user(
            name="Outro Usuario",
            email=" MACAYA@EXAMPLE.COM ",
            password="Senha5678",
        )


def test_login_normalizes_email():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    service.create_user(
        name="Macaya", email="macaya@example.com", password="SecurePass123!"
    )

    # Assert
    assert service.login(" MACAYA@EXAMPLE.COM ", "SecurePass123!") is True


def test_login_with_wrong_password():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    service.create_user(
        name="Macaya", email="macaya@example.com", password="Macaya@1234!"
    )

    # Assert
    assert service.login(" MACAYA@EXAMPLE.COM ", "Macaya!1234@") is False


def test_login_with_nonexistent_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    resultado = service.login("naoexiste@example.com", "Macaya@1234!")

    # Assert
    assert resultado is False


def test_login_with_inactive_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Macaya@1234!",
    )
    service.deactivate(
        email="macaya@example.com",
    )

    # Assert
    assert service.login("macaya@example.com", "Macaya@1234!") is False


def test_update_user_name():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act
    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Macaya@1234!",
    )
    service.update_name(
        email="macaya@example.com",
        new_name="Macaynha",
    )

    # Assert
    usuario = repo.get_by_email(email="macaya@example.com")
    assert usuario.name == "Macaynha"


def test_update_name_with_nonexistent_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act + Assert
    with pytest.raises(ValueError, match="Usuário não encontrado."):
        service.update_name(
            email="nothingthere@example.com",
            new_name="Macaya",
        )
