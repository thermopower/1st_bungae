# tests/integration/services/test_application_service.py
"""
ApplicationService 통합 테스트
"""

import pytest
from datetime import datetime, date
from unittest.mock import Mock, MagicMock

from app.application.services.application_service import ApplicationService
from app.domain.entities.application import Application
from app.domain.entities.campaign import Campaign, CampaignStatus
from app.domain.entities.influencer import Influencer
from app.domain.exceptions.application_exceptions import (
    AlreadyAppliedException,
    CampaignNotRecruitingException,
    InfluencerNotRegisteredException,
)
from app.shared.constants.campaign_constants import APPLICATION_STATUS_APPLIED


class TestApplicationServiceApply:
    """ApplicationService.apply_to_campaign() 통합 테스트"""

    def test_apply_to_campaign_creates_application_when_valid(self):
        """정상적인 조건에서 체험단 지원 시 Application 생성"""
        # Arrange
        campaign_id = 1
        influencer_id = 1
        application_reason = "체험단에 지원합니다."

        campaign = Campaign(
            id=campaign_id,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="혜택",
            conditions="조건",
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )

        influencer = Influencer(
            id=influencer_id,
            user_id="test-user-id",
            name="테스트",
            birth_date=date(1990, 1, 1),
            phone_number="010-1234-5678",
            channel_name="채널",
            channel_url="https://example.com",
            follower_count=1000,
            created_at=datetime.now()
        )

        # Mock repositories
        mock_application_repo = Mock()
        mock_campaign_repo = Mock()
        mock_influencer_repo = Mock()

        mock_campaign_repo.find_by_id.return_value = campaign
        mock_influencer_repo.find_by_id.return_value = influencer
        mock_application_repo.exists_by_campaign_and_influencer.return_value = False
        mock_application_repo.save.return_value = Application(
            id=1,
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            application_reason=application_reason,
            status=APPLICATION_STATUS_APPLIED,
            applied_at=datetime.now()
        )

        service = ApplicationService(
            mock_application_repo,
            mock_campaign_repo,
            mock_influencer_repo
        )

        # Act
        result = service.apply_to_campaign(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            application_reason=application_reason
        )

        # Assert
        assert result is not None
        assert result.campaign_id == campaign_id
        assert result.influencer_id == influencer_id
        assert result.status == APPLICATION_STATUS_APPLIED
        mock_application_repo.save.assert_called_once()

    def test_apply_to_campaign_raises_when_influencer_not_found(self):
        """인플루언서 정보가 없을 때 예외 발생"""
        # Arrange
        campaign_id = 1
        influencer_id = 999  # 존재하지 않는 ID

        mock_application_repo = Mock()
        mock_campaign_repo = Mock()
        mock_influencer_repo = Mock()

        mock_influencer_repo.find_by_id.return_value = None

        service = ApplicationService(
            mock_application_repo,
            mock_campaign_repo,
            mock_influencer_repo
        )

        # Act & Assert
        with pytest.raises(InfluencerNotRegisteredException):
            service.apply_to_campaign(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                application_reason=None
            )

    def test_apply_to_campaign_raises_when_campaign_not_recruiting(self):
        """체험단이 모집 중이 아닐 때 예외 발생"""
        # Arrange
        campaign_id = 1
        influencer_id = 1

        campaign = Campaign(
            id=campaign_id,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="혜택",
            conditions="조건",
            image_url=None,
            status=CampaignStatus.CLOSED,  # 모집 종료
            created_at=datetime.now(),
            closed_at=datetime.now()
        )

        influencer = Influencer(
            id=influencer_id,
            user_id="test-user-id",
            name="테스트",
            birth_date=date(1990, 1, 1),
            phone_number="010-1234-5678",
            channel_name="채널",
            channel_url="https://example.com",
            follower_count=1000,
            created_at=datetime.now()
        )

        mock_application_repo = Mock()
        mock_campaign_repo = Mock()
        mock_influencer_repo = Mock()

        mock_campaign_repo.find_by_id.return_value = campaign
        mock_influencer_repo.find_by_id.return_value = influencer

        service = ApplicationService(
            mock_application_repo,
            mock_campaign_repo,
            mock_influencer_repo
        )

        # Act & Assert
        with pytest.raises(CampaignNotRecruitingException):
            service.apply_to_campaign(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                application_reason=None
            )

    def test_apply_to_campaign_raises_when_already_applied(self):
        """이미 지원한 경우 예외 발생"""
        # Arrange
        campaign_id = 1
        influencer_id = 1

        campaign = Campaign(
            id=campaign_id,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="혜택",
            conditions="조건",
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )

        influencer = Influencer(
            id=influencer_id,
            user_id="test-user-id",
            name="테스트",
            birth_date=date(1990, 1, 1),
            phone_number="010-1234-5678",
            channel_name="채널",
            channel_url="https://example.com",
            follower_count=1000,
            created_at=datetime.now()
        )

        mock_application_repo = Mock()
        mock_campaign_repo = Mock()
        mock_influencer_repo = Mock()

        mock_campaign_repo.find_by_id.return_value = campaign
        mock_influencer_repo.find_by_id.return_value = influencer
        mock_application_repo.exists_by_campaign_and_influencer.return_value = True  # 이미 지원함

        service = ApplicationService(
            mock_application_repo,
            mock_campaign_repo,
            mock_influencer_repo
        )

        # Act & Assert
        with pytest.raises(AlreadyAppliedException):
            service.apply_to_campaign(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                application_reason=None
            )
