"""
Auth Exceptions

인증/인가 실패 시 발생하는 예외들
"""

from app.domain.exceptions.base import DomainException


class AuthException(DomainException):
    """
    인증/인가 실패 예외

    HTTP Status Code: 401 Unauthorized
    """

    def __init__(self, message: str):
        """
        AuthException 초기화

        Args:
            message: 예외 메시지
        """
        super().__init__(message=message, http_status_code=401)


class InvalidCredentialsException(AuthException):
    """
    잘못된 인증 정보 예외

    이메일 또는 비밀번호가 잘못된 경우 발생

    HTTP Status Code: 401 Unauthorized
    """

    def __init__(self):
        """InvalidCredentialsException 초기화"""
        message = "Invalid credentials"
        super().__init__(message=message)


class EmailAlreadyExistsException(DomainException):
    """
    이메일 중복 예외

    이미 등록된 이메일로 회원가입을 시도한 경우 발생

    HTTP Status Code: 409 Conflict
    """

    def __init__(self, email: str):
        """
        EmailAlreadyExistsException 초기화

        Args:
            email: 중복된 이메일 주소
        """
        message = f"Email already registered: {email}"
        super().__init__(message=message, http_status_code=409)


class UnauthorizedException(DomainException):
    """
    권한 없음 예외

    접근 권한이 없는 리소스에 접근을 시도한 경우 발생

    HTTP Status Code: 403 Forbidden
    """

    def __init__(self):
        """UnauthorizedException 초기화"""
        message = "Unauthorized access"
        super().__init__(message=message, http_status_code=403)
