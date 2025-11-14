"""
Domain Exceptions

도메인 계층에서 발생하는 예외 정의
"""

from app.domain.exceptions.base import DomainException
from app.domain.exceptions.validation_exceptions import (
    InvalidBusinessNumberException,
    InvalidEmailException,
    InvalidPhoneNumberException,
    ValidationException,
)
from app.domain.exceptions.auth_exceptions import (
    AuthException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    UnauthorizedException,
)
from app.domain.exceptions.advertiser_exceptions import (
    AdvertiserAlreadyRegisteredException,
    BusinessNumberAlreadyExistsException,
)

__all__ = [
    # Base Exception
    "DomainException",
    # Validation Exceptions
    "ValidationException",
    "InvalidEmailException",
    "InvalidPhoneNumberException",
    "InvalidBusinessNumberException",
    # Auth Exceptions
    "AuthException",
    "InvalidCredentialsException",
    "EmailAlreadyExistsException",
    "UnauthorizedException",
    # Advertiser Exceptions
    "AdvertiserAlreadyRegisteredException",
    "BusinessNumberAlreadyExistsException",
]
