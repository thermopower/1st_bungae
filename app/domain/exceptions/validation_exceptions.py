"""
Validation Exceptions

입력값 검증 실패 시 발생하는 예외들
"""

from app.domain.exceptions.base import DomainException


class ValidationException(DomainException):
    """
    검증 실패 예외

    HTTP Status Code: 400 Bad Request
    """

    def __init__(self, message: str):
        """
        ValidationException 초기화

        Args:
            message: 예외 메시지
        """
        super().__init__(message=message, http_status_code=400)


class InvalidEmailException(ValidationException):
    """
    이메일 형식 검증 실패 예외

    Args:
        email: 잘못된 이메일 값
    """

    def __init__(self, email: str):
        """
        InvalidEmailException 초기화

        Args:
            email: 잘못된 이메일 값
        """
        message = f"Invalid email format: {email}"
        super().__init__(message=message)


class InvalidPhoneNumberException(ValidationException):
    """
    전화번호 형식 검증 실패 예외

    Args:
        phone_number: 잘못된 전화번호 값
    """

    def __init__(self, phone_number: str):
        """
        InvalidPhoneNumberException 초기화

        Args:
            phone_number: 잘못된 전화번호 값
        """
        message = f"Invalid phone number format: {phone_number}"
        super().__init__(message=message)


class InvalidBusinessNumberException(ValidationException):
    """
    사업자등록번호 검증 실패 예외

    Args:
        business_number: 잘못된 사업자등록번호 값
    """

    def __init__(self, business_number: str):
        """
        InvalidBusinessNumberException 초기화

        Args:
            business_number: 잘못된 사업자등록번호 값
        """
        message = f"Invalid business number: {business_number}"
        super().__init__(message=message)
