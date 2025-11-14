# app/domain/exceptions/application_exceptions.py
"""
Application 도메인 예외
체험단 지원 관련 비즈니스 규칙 위반 시 발생하는 예외
"""

from app.domain.exceptions.base import DomainException


class AlreadyAppliedException(DomainException):
    """중복 지원"""
    pass


class CampaignNotRecruitingException(DomainException):
    """모집 종료된 체험단"""
    pass


class InfluencerNotRegisteredException(DomainException):
    """인플루언서 정보 미등록"""
    pass
