"""
ApplicationRules 단위 테스트
"""

import pytest
from datetime import datetime, date
from app.domain.business_rules.application_rules import ApplicationRules
from app.domain.entities.campaign import Campaign, CampaignStatus
from app.domain.entities.influencer import Influencer


class TestApplicationRules:
    """ApplicationRules 단위 테스트"""

    def test_can_apply_returns_true_when_campaign_is_recruiting(self):
        """체험단이 모집 중일 때 can_apply가 (True, None) 반환"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트 설명",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="테스트 혜택",
            conditions="테스트 조건",
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )
        influencer = Influencer(
            id=1,
            user_id="test-user-id",
            name="테스트 인플루언서",
            birth_date=date(1990, 1, 1),
            phone_number="010-1234-5678",
            channel_name="테스트 채널",
            channel_url="https://example.com",
            follower_count=1000,
            created_at=datetime.now()
        )
        already_applied = False

        # Act
        can_apply, error_message = ApplicationRules.can_apply(
            campaign, influencer, already_applied
        )

        # Assert
        assert can_apply is True
        assert error_message is None

    def test_can_apply_returns_false_when_campaign_is_closed(self):
        """체험단이 모집 종료 상태일 때 can_apply가 (False, 에러 메시지) 반환"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트 설명",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="테스트 혜택",
            conditions="테스트 조건",
            image_url=None,
            status=CampaignStatus.CLOSED,
            created_at=datetime.now(),
            closed_at=datetime.now()
        )
        influencer = Influencer(
            id=1,
            user_id="test-user-id",
            name="테스트 인플루언서",
            birth_date=date(1990, 1, 1),
            phone_number="010-1234-5678",
            channel_name="테스트 채널",
            channel_url="https://example.com",
            follower_count=1000,
            created_at=datetime.now()
        )
        already_applied = False

        # Act
        can_apply, error_message = ApplicationRules.can_apply(
            campaign, influencer, already_applied
        )

        # Assert
        assert can_apply is False
        assert error_message == "모집이 종료된 체험단입니다"

    def test_can_apply_returns_false_when_already_applied(self):
        """이미 지원한 경우 can_apply가 (False, 에러 메시지) 반환"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트 설명",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="테스트 혜택",
            conditions="테스트 조건",
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )
        influencer = Influencer(
            id=1,
            user_id="test-user-id",
            name="테스트 인플루언서",
            birth_date=date(1990, 1, 1),
            phone_number="010-1234-5678",
            channel_name="테스트 채널",
            channel_url="https://example.com",
            follower_count=1000,
            created_at=datetime.now()
        )
        already_applied = True

        # Act
        can_apply, error_message = ApplicationRules.can_apply(
            campaign, influencer, already_applied
        )

        # Assert
        assert can_apply is False
        assert error_message == "이미 지원한 체험단입니다"

    def test_can_apply_returns_false_when_influencer_is_none(self):
        """인플루언서 정보가 없을 때 can_apply가 (False, 에러 메시지) 반환"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=1,
            title="테스트 체험단",
            description="테스트 설명",
            quota=5,
            start_date=date.today(),
            end_date=date.today(),
            benefits="테스트 혜택",
            conditions="테스트 조건",
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )
        influencer = None
        already_applied = False

        # Act
        can_apply, error_message = ApplicationRules.can_apply(
            campaign, influencer, already_applied
        )

        # Assert
        assert can_apply is False
        assert error_message == "인플루언서 정보가 등록되지 않았습니다"
