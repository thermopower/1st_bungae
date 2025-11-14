"""
Auth Exception 테스트

RED Phase: 실패하는 테스트 먼저 작성
"""

import pytest


class TestAuthException:
    """AuthException 테스트"""

    def test_auth_exception_can_be_raised(self):
        """
        정상 케이스: AuthException을 발생시킬 수 있어야 함

        Given: AuthException 클래스
        When: 메시지와 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포함됨
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import AuthException

        # Act & Assert
        with pytest.raises(AuthException) as exc_info:
            raise AuthException("Authentication failed")

        assert str(exc_info.value) == "Authentication failed"
        assert exc_info.value.message == "Authentication failed"

    def test_auth_exception_is_subclass_of_domain_exception(self):
        """
        AuthException은 DomainException의 서브클래스여야 함

        Given: AuthException 클래스
        When: issubclass 검사
        Then: DomainException의 서브클래스여야 함
        """
        # Arrange
        from app.domain.exceptions.base import DomainException
        from app.domain.exceptions.auth_exceptions import AuthException

        # Act & Assert
        assert issubclass(AuthException, DomainException)

    def test_auth_exception_has_http_status_code_401(self):
        """
        AuthException은 http_status_code 401을 가져야 함

        Given: AuthException 클래스
        When: http_status_code 속성 접근
        Then: 401 반환
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import AuthException

        # Act
        exception = AuthException("Authentication failed")

        # Assert
        assert exception.http_status_code == 401


class TestInvalidCredentialsException:
    """InvalidCredentialsException 테스트"""

    def test_invalid_credentials_exception_can_be_raised(self):
        """
        정상 케이스: InvalidCredentialsException을 발생시킬 수 있어야 함

        Given: InvalidCredentialsException 클래스
        When: 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포맷팅됨
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import InvalidCredentialsException

        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            raise InvalidCredentialsException()

        assert "Invalid credentials" in str(exc_info.value)

    def test_invalid_credentials_exception_is_subclass_of_auth_exception(self):
        """
        InvalidCredentialsException은 AuthException의 서브클래스여야 함

        Given: InvalidCredentialsException 클래스
        When: issubclass 검사
        Then: AuthException의 서브클래스여야 함
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import (
            AuthException,
            InvalidCredentialsException,
        )

        # Act & Assert
        assert issubclass(InvalidCredentialsException, AuthException)


class TestEmailAlreadyExistsException:
    """EmailAlreadyExistsException 테스트"""

    def test_email_already_exists_exception_can_be_raised(self):
        """
        정상 케이스: EmailAlreadyExistsException을 발생시킬 수 있어야 함

        Given: EmailAlreadyExistsException 클래스
        When: 이메일 값과 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포맷팅됨
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import EmailAlreadyExistsException

        # Act & Assert
        with pytest.raises(EmailAlreadyExistsException) as exc_info:
            raise EmailAlreadyExistsException("test@example.com")

        assert "Email already registered" in str(exc_info.value)
        assert "test@example.com" in str(exc_info.value)

    def test_email_already_exists_exception_has_http_status_code_409(self):
        """
        EmailAlreadyExistsException은 http_status_code 409를 가져야 함

        Given: EmailAlreadyExistsException 클래스
        When: http_status_code 속성 접근
        Then: 409 반환
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import EmailAlreadyExistsException

        # Act
        exception = EmailAlreadyExistsException("test@example.com")

        # Assert
        assert exception.http_status_code == 409


class TestUnauthorizedException:
    """UnauthorizedException 테스트"""

    def test_unauthorized_exception_can_be_raised(self):
        """
        정상 케이스: UnauthorizedException을 발생시킬 수 있어야 함

        Given: UnauthorizedException 클래스
        When: 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포맷팅됨
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import UnauthorizedException

        # Act & Assert
        with pytest.raises(UnauthorizedException) as exc_info:
            raise UnauthorizedException()

        assert "Unauthorized access" in str(exc_info.value)

    def test_unauthorized_exception_has_http_status_code_403(self):
        """
        UnauthorizedException은 http_status_code 403을 가져야 함

        Given: UnauthorizedException 클래스
        When: http_status_code 속성 접근
        Then: 403 반환
        """
        # Arrange
        from app.domain.exceptions.auth_exceptions import UnauthorizedException

        # Act
        exception = UnauthorizedException()

        # Assert
        assert exception.http_status_code == 403
