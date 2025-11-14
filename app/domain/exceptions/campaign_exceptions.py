# app/domain/exceptions/campaign_exceptions.py
"""
Campaign 도메인 예외
체험단 관련 비즈니스 규칙 위반 시 발생하는 예외
"""

from app.domain.exceptions.base import DomainException


class CampaignNotFoundException(DomainException):
    """체험단을 찾을 수 없음"""
    pass


class CampaignAlreadyClosedException(DomainException):
    """이미 종료된 체험단"""
    pass


class CampaignNotOwnedException(DomainException):
    """체험단 소유권 없음"""
    pass


class InvalidCampaignStatusException(DomainException):
    """잘못된 체험단 상태"""
    pass


class SelectionQuotaExceededException(DomainException):
    """선정 인원 초과"""
    pass
