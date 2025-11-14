# tests/unit/domain/exceptions/test_campaign_exceptions.py
"""
Campaign Exceptions 단위 테스트
TDD Red Phase: 실패하는 테스트 먼저 작성
"""

import pytest
from app.domain.exceptions.campaign_exceptions import (
    CampaignNotFoundException,
    CampaignAlreadyClosedException,
    CampaignNotOwnedException,
    InvalidCampaignStatusException,
    SelectionQuotaExceededException
)
from app.domain.exceptions.base import DomainException


class TestCampaignExceptions:
    """Campaign 예외 테스트"""

    def test_campaign_not_found_exception_is_domain_exception(self):
        """CampaignNotFoundException이 DomainException을 상속하는지 확인"""
        # Arrange & Act
        exception = CampaignNotFoundException("체험단을 찾을 수 없습니다.")

        # Assert
        assert isinstance(exception, DomainException)
        assert str(exception) == "체험단을 찾을 수 없습니다."

    def test_campaign_already_closed_exception_has_message(self):
        """CampaignAlreadyClosedException이 메시지를 가지는지 확인"""
        # Arrange & Act
        exception = CampaignAlreadyClosedException("이미 종료된 체험단입니다.")

        # Assert
        assert str(exception) == "이미 종료된 체험단입니다."

    def test_campaign_not_owned_exception_can_be_raised(self):
        """CampaignNotOwnedException이 발생할 수 있는지 확인"""
        # Arrange & Act & Assert
        with pytest.raises(CampaignNotOwnedException) as exc_info:
            raise CampaignNotOwnedException("체험단 소유권이 없습니다.")

        assert "체험단 소유권이 없습니다." in str(exc_info.value)

    def test_invalid_campaign_status_exception_can_be_raised(self):
        """InvalidCampaignStatusException이 발생할 수 있는지 확인"""
        # Arrange & Act & Assert
        with pytest.raises(InvalidCampaignStatusException) as exc_info:
            raise InvalidCampaignStatusException("잘못된 체험단 상태입니다.")

        assert "잘못된 체험단 상태입니다." in str(exc_info.value)

    def test_selection_quota_exceeded_exception_can_be_raised(self):
        """SelectionQuotaExceededException이 발생할 수 있는지 확인"""
        # Arrange & Act & Assert
        with pytest.raises(SelectionQuotaExceededException) as exc_info:
            raise SelectionQuotaExceededException("선정 인원이 모집 인원을 초과했습니다.")

        assert "선정 인원이 모집 인원을 초과했습니다." in str(exc_info.value)
