# tests/unit/domain/business_rules/test_campaign_rules.py
"""
Campaign Business Rules 단위 테스트
TDD Red Phase: 실패하는 테스트 먼저 작성
"""

import pytest
from datetime import date, datetime
from app.domain.entities.campaign import Campaign, CampaignStatus
from app.domain.business_rules.campaign_rules import CampaignRules


class TestCampaignRules:
    """Campaign 비즈니스 규칙 테스트"""

    def test_can_close_early_returns_true_when_recruiting(self):
        """모집 중 상태일 때 조기종료 가능"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=10,
            title='테스트 체험단',
            description='설명',
            quota=5,
            start_date=date(2025, 11, 15),
            end_date=date(2025, 11, 30),
            benefits='혜택',
            conditions='조건',
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )

        # Act
        result = CampaignRules.can_close_early(campaign)

        # Assert
        assert result is True

    def test_can_close_early_returns_false_when_already_closed(self):
        """이미 종료된 체험단은 조기종료 불가"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=10,
            title='테스트 체험단',
            description='설명',
            quota=5,
            start_date=date(2025, 11, 15),
            end_date=date(2025, 11, 30),
            benefits='혜택',
            conditions='조건',
            image_url=None,
            status=CampaignStatus.CLOSED,
            created_at=datetime.now(),
            closed_at=datetime.now()
        )

        # Act
        result = CampaignRules.can_close_early(campaign)

        # Assert
        assert result is False

    def test_can_select_influencers_returns_true_when_closed(self):
        """모집 종료 상태일 때 인플루언서 선정 가능"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=10,
            title='테스트 체험단',
            description='설명',
            quota=5,
            start_date=date(2025, 11, 15),
            end_date=date(2025, 11, 30),
            benefits='혜택',
            conditions='조건',
            image_url=None,
            status=CampaignStatus.CLOSED,
            created_at=datetime.now(),
            closed_at=datetime.now()
        )

        # Act
        result = CampaignRules.can_select_influencers(campaign)

        # Assert
        assert result is True

    def test_can_select_influencers_returns_false_when_recruiting(self):
        """모집 중일 때 인플루언서 선정 불가"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=10,
            title='테스트 체험단',
            description='설명',
            quota=5,
            start_date=date(2025, 11, 15),
            end_date=date(2025, 11, 30),
            benefits='혜택',
            conditions='조건',
            image_url=None,
            status=CampaignStatus.RECRUITING,
            created_at=datetime.now(),
            closed_at=None
        )

        # Act
        result = CampaignRules.can_select_influencers(campaign)

        # Assert
        assert result is False

    def test_validate_selection_count_returns_true_when_within_quota(self):
        """선정 인원이 모집 인원 이하일 때 검증 통과"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=10,
            title='테스트 체험단',
            description='설명',
            quota=5,
            start_date=date(2025, 11, 15),
            end_date=date(2025, 11, 30),
            benefits='혜택',
            conditions='조건',
            image_url=None,
            status=CampaignStatus.CLOSED,
            created_at=datetime.now(),
            closed_at=datetime.now()
        )
        selected_count = 3

        # Act
        result = CampaignRules.validate_selection_count(campaign, selected_count)

        # Assert
        assert result is True

    def test_validate_selection_count_returns_false_when_exceeds_quota(self):
        """선정 인원이 모집 인원 초과 시 검증 실패"""
        # Arrange
        campaign = Campaign(
            id=1,
            advertiser_id=10,
            title='테스트 체험단',
            description='설명',
            quota=5,
            start_date=date(2025, 11, 15),
            end_date=date(2025, 11, 30),
            benefits='혜택',
            conditions='조건',
            image_url=None,
            status=CampaignStatus.CLOSED,
            created_at=datetime.now(),
            closed_at=datetime.now()
        )
        selected_count = 6

        # Act
        result = CampaignRules.validate_selection_count(campaign, selected_count)

        # Assert
        assert result is False

    def test_validate_campaign_dates_returns_true_when_valid(self):
        """모집 기간이 유효할 때 검증 통과"""
        # Arrange
        today = date.today()
        start_date = date(2025, 12, 1)
        end_date = date(2025, 12, 31)

        # Act
        result = CampaignRules.validate_campaign_dates(start_date, end_date)

        # Assert
        assert result is True

    def test_validate_campaign_dates_returns_false_when_start_date_is_past(self):
        """시작일이 과거일 때 검증 실패"""
        # Arrange
        start_date = date(2020, 1, 1)
        end_date = date(2025, 12, 31)

        # Act
        result = CampaignRules.validate_campaign_dates(start_date, end_date)

        # Assert
        assert result is False

    def test_validate_campaign_dates_returns_false_when_end_before_start(self):
        """종료일이 시작일보다 앞설 때 검증 실패"""
        # Arrange
        start_date = date(2025, 12, 31)
        end_date = date(2025, 12, 1)

        # Act
        result = CampaignRules.validate_campaign_dates(start_date, end_date)

        # Assert
        assert result is False
