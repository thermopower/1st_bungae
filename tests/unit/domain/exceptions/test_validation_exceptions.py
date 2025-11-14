"""
Validation Exception 테스트

RED Phase: 실패하는 테스트 먼저 작성
"""

import pytest


class TestValidationException:
    """ValidationException 테스트"""

    def test_validation_exception_can_be_raised(self):
        """
        정상 케이스: ValidationException을 발생시킬 수 있어야 함

        Given: ValidationException 클래스
        When: 메시지와 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포함됨
        """
        # Arrange
        from app.domain.exceptions.validation_exceptions import ValidationException

        # Act & Assert
        with pytest.raises(ValidationException) as exc_info:
            raise ValidationException("Invalid data")

        assert str(exc_info.value) == "Invalid data"
        assert exc_info.value.message == "Invalid data"

    def test_validation_exception_is_subclass_of_domain_exception(self):
        """
        ValidationException은 DomainException의 서브클래스여야 함

        Given: ValidationException 클래스
        When: issubclass 검사
        Then: DomainException의 서브클래스여야 함
        """
        # Arrange
        from app.domain.exceptions.base import DomainException
        from app.domain.exceptions.validation_exceptions import ValidationException

        # Act & Assert
        assert issubclass(ValidationException, DomainException)

    def test_validation_exception_has_http_status_code_400(self):
        """
        ValidationException은 http_status_code 400을 가져야 함

        Given: ValidationException 클래스
        When: http_status_code 속성 접근
        Then: 400 반환
        """
        # Arrange
        from app.domain.exceptions.validation_exceptions import ValidationException

        # Act
        exception = ValidationException("Invalid data")

        # Assert
        assert exception.http_status_code == 400


class TestInvalidEmailException:
    """InvalidEmailException 테스트"""

    def test_invalid_email_exception_can_be_raised(self):
        """
        정상 케이스: InvalidEmailException을 발생시킬 수 있어야 함

        Given: InvalidEmailException 클래스
        When: 이메일 값과 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포맷팅됨
        """
        # Arrange
        from app.domain.exceptions.validation_exceptions import InvalidEmailException

        # Act & Assert
        with pytest.raises(InvalidEmailException) as exc_info:
            raise InvalidEmailException("test@invalid")

        assert "Invalid email format" in str(exc_info.value)
        assert "test@invalid" in str(exc_info.value)

    def test_invalid_email_exception_is_subclass_of_validation_exception(self):
        """
        InvalidEmailException은 ValidationException의 서브클래스여야 함

        Given: InvalidEmailException 클래스
        When: issubclass 검사
        Then: ValidationException의 서브클래스여야 함
        """
        # Arrange
        from app.domain.exceptions.validation_exceptions import (
            InvalidEmailException,
            ValidationException,
        )

        # Act & Assert
        assert issubclass(InvalidEmailException, ValidationException)


class TestInvalidPhoneNumberException:
    """InvalidPhoneNumberException 테스트"""

    def test_invalid_phone_number_exception_can_be_raised(self):
        """
        정상 케이스: InvalidPhoneNumberException을 발생시킬 수 있어야 함

        Given: InvalidPhoneNumberException 클래스
        When: 전화번호 값과 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포맷팅됨
        """
        # Arrange
        from app.domain.exceptions.validation_exceptions import InvalidPhoneNumberException

        # Act & Assert
        with pytest.raises(InvalidPhoneNumberException) as exc_info:
            raise InvalidPhoneNumberException("010-12-34")

        assert "Invalid phone number format" in str(exc_info.value)
        assert "010-12-34" in str(exc_info.value)


class TestInvalidBusinessNumberException:
    """InvalidBusinessNumberException 테스트"""

    def test_invalid_business_number_exception_can_be_raised(self):
        """
        정상 케이스: InvalidBusinessNumberException을 발생시킬 수 있어야 함

        Given: InvalidBusinessNumberException 클래스
        When: 사업자번호 값과 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포맷팅됨
        """
        # Arrange
        from app.domain.exceptions.validation_exceptions import (
            InvalidBusinessNumberException,
        )

        # Act & Assert
        with pytest.raises(InvalidBusinessNumberException) as exc_info:
            raise InvalidBusinessNumberException("123456789")

        assert "Invalid business number" in str(exc_info.value)
        assert "123456789" in str(exc_info.value)
