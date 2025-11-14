"""
Domain Base Exception 테스트

RED Phase: 실패하는 테스트 먼저 작성
"""

import pytest


class TestDomainException:
    """DomainException 베이스 클래스 테스트"""

    def test_domain_exception_can_be_raised(self):
        """
        정상 케이스: DomainException을 발생시킬 수 있어야 함

        Given: DomainException 클래스
        When: 메시지와 함께 예외 발생
        Then: 예외가 정상적으로 발생하고 메시지가 포함됨
        """
        # Arrange
        from app.domain.exceptions.base import DomainException

        # Act & Assert
        with pytest.raises(DomainException) as exc_info:
            raise DomainException("Test error message")

        assert str(exc_info.value) == "Test error message"
        assert exc_info.value.message == "Test error message"

    def test_domain_exception_is_subclass_of_exception(self):
        """
        DomainException은 Python Exception의 서브클래스여야 함

        Given: DomainException 클래스
        When: issubclass 검사
        Then: Exception의 서브클래스여야 함
        """
        # Arrange
        from app.domain.exceptions.base import DomainException

        # Act & Assert
        assert issubclass(DomainException, Exception)

    def test_domain_exception_has_http_status_code(self):
        """
        DomainException은 http_status_code 속성을 가져야 함

        Given: DomainException 클래스
        When: http_status_code 속성 접근
        Then: 기본값 500 반환
        """
        # Arrange
        from app.domain.exceptions.base import DomainException

        # Act
        exception = DomainException("Test error")

        # Assert
        assert hasattr(exception, "http_status_code")
        assert exception.http_status_code == 500

    def test_domain_exception_message_cannot_be_empty(self):
        """
        에러 케이스: DomainException 메시지는 비어있을 수 없음

        Given: 빈 메시지
        When: DomainException 생성
        Then: ValueError 발생
        """
        # Arrange
        from app.domain.exceptions.base import DomainException

        # Act & Assert
        with pytest.raises(ValueError, match="Error message cannot be empty"):
            DomainException("")

    def test_domain_exception_message_cannot_be_none(self):
        """
        에러 케이스: DomainException 메시지는 None일 수 없음

        Given: None 메시지
        When: DomainException 생성
        Then: ValueError 발생
        """
        # Arrange
        from app.domain.exceptions.base import DomainException

        # Act & Assert
        with pytest.raises(ValueError, match="Error message cannot be empty"):
            DomainException(None)
