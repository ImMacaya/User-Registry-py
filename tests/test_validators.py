import pytest
from src.user_registry.service.user_service import UserService
from tests.test_user_service import FakeUserRepository
from user_registry.domain.validators import (
    normalize_email,
    validate_email,
    validate_name,
    validate_password,
)


def test_validate_email_ok():
    validate_email("a@b.com")


def test_validate_email_fail():
    with pytest.raises(ValueError):
        validate_email("invalido")


def test_validate_password_fail():
    with pytest.raises(ValueError):
        validate_password("123")


def test_validate_name_ok():
    validate_name("Daniel")


def test_validate_name_fail_empty():
    with pytest.raises(ValueError):
        validate_name("")


def test_validate_name_fail_too_short():
    with pytest.raises(ValueError):
        validate_name("A")


def test_normalize_email_uppercase():
    # Arrange
    email = "MACAYA@EXAMPLE.COM"

    # Act
    result = normalize_email(email)

    # Assert
    assert result == "macaya@example.com"


def test_normalize_email_whitespace():
    # Arrange
    email = " macaya@example.com "

    # Act
    result = normalize_email(email)

    # Assert
    assert result == "macaya@example.com"


def test_normalize_email_mixed_case_and_whitespace():
    # Arrange
    email = " MACAYA@EXAMPLE.COM "

    # Act
    result = normalize_email(email)

    # Assert
    assert result == "macaya@example.com"
