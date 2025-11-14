"""광고주 도메인 예외"""

from app.domain.exceptions.base import DomainException


class AdvertiserAlreadyRegisteredException(DomainException):
    """광고주 정보 이미 등록됨 예외"""
    pass


class BusinessNumberAlreadyExistsException(DomainException):
    """사업자등록번호 중복 예외"""
    pass
