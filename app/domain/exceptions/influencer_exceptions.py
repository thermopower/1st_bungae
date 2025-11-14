"""
인플루언서 관련 도메인 예외
"""
from app.domain.exceptions.base import DomainException


class InfluencerAlreadyRegisteredException(DomainException):
    """인플루언서가 이미 등록된 경우 발생하는 예외"""
    pass


class InfluencerNotFoundException(DomainException):
    """인플루언서를 찾을 수 없는 경우 발생하는 예외"""
    pass
