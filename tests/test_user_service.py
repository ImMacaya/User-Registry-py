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
            name="Super Macaya",
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
    result = service.login("naoexiste@example.com", "Macaya@1234!")

    # Assert
    assert result is False


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
    user = repo.get_by_email(email="macaya@example.com")
    assert user.name == "Macaynha"


def test_update_name_with_nonexistent_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act + Assert
    with pytest.raises(ValueError, match=r"^Usuário não encontrado\.$"):
        service.update_name(
            email="nothingthere@example.com",
            new_name="Macaya",
        )


def test_deactivate_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Macaya@1234!",
    )

    # Act
    service.deactivate(
        email="macaya@example.com",
    )

    # Assert
    user = repo.get_by_email(email="macaya@example.com")
    assert user is not None
    assert user.is_active is False


def test_deactivate_nonexistent_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act + Assert
    with pytest.raises(ValueError, match=r"^Usuário não encontrado\.$"):
        service.deactivate(email="nothingthere@example.com")


def test_activate_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    service.create_user(
        name="Macaya", email="macaya@example.com", password="Macaya@1234!"
    )

    service.deactivate(email="macaya@example.com")

    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is False

    # Act
    service.activate(email="macaya@example.com")

    # Assert
    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is True


def test_activate_nonexistent_user():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    # Act + Assert
    with pytest.raises(ValueError, match=r"^Usuário não encontrado\.$"):
        service.activate(email="nothingthere@example.com")


def test_update_name_normalizes_email():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Macaya@1234!",
    )

    # Act
    service.update_name(
        email=" MACAYA@EXAMPLE.COM ",
        new_name="Macacaya",
    )

    # Assert
    user = repo.get_by_email(email="macaya@example.com")
    assert user is not None
    assert user.name == "Macacaya"


def test_deactivate_normalizes_email():
    # Arrange

    repo = FakeUserRepository()
    service = UserService(repo)

    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Macaya@1234!",
    )

    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is True

    # Act
    service.deactivate(email=" MACAYA@EXAMPLE.COM ")

    # Assert
    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is False


def test_activate_normalizes_email():
    # Arrange
    repo = FakeUserRepository()
    service = UserService(repo)

    service.create_user(
        name="Macaya",
        email="macaya@example.com",
        password="Macaya@1234!",
    )

    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is True

    service.deactivate(email="macaya@example.com")

    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is False

    # Act
    service.activate(email=" MACAYA@EXAMPLE.COM ")

    # Assert
    user = repo.get_by_email("macaya@example.com")
    assert user is not None
    assert user.is_active is True
