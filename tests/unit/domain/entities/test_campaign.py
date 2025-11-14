# tests/unit/domain/entities/test_campaign.py
"""
Campaign Entity 단위 테스트
TDD Red Phase: 실패하는 테스트 먼저 작성
"""

import pytest
from datetime import date, datetime
from app.domain.entities.campaign import Campaign, CampaignStatus


class TestCampaignEntity:
    """Campaign 엔티티 테스트"""

    def test_campaign_creation_with_valid_data(self):
        """정상적인 데이터로 Campaign 생성"""
        # Arrange
        campaign_data = {
            'id': 1,
            'advertiser_id': 10,
            'title': '신메뉴 파스타 체험단 모집',
            'description': '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
            'quota': 5,
            'start_date': date(2025, 11, 15),
            'end_date': date(2025, 11, 30),
            'benefits': '무료 식사 제공',
            'conditions': '인스타그램 피드 1개 + 스토리 2개 업로드',
            'image_url': 'https://example.com/image.jpg',
            'status': CampaignStatus.RECRUITING,
            'created_at': datetime(2025, 11, 14, 10, 0, 0),
            'closed_at': None
        }

        # Act
        campaign = Campaign(**campaign_data)

        # Assert
        assert campaign.id == 1
        assert campaign.advertiser_id == 10
        assert campaign.title == '신메뉴 파스타 체험단 모집'
        assert campaign.quota == 5
        assert campaign.status == CampaignStatus.RECRUITING

    def test_campaign_is_recruiting_returns_true_when_status_is_recruiting(self):
        """모집 중 상태일 때 is_recruiting()이 True 반환"""
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
        result = campaign.is_recruiting()

        # Assert
        assert result is True

    def test_campaign_is_recruiting_returns_false_when_status_is_closed(self):
        """모집 종료 상태일 때 is_recruiting()이 False 반환"""
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
        result = campaign.is_recruiting()

        # Assert
        assert result is False

    def test_campaign_is_selected_returns_true_when_status_is_selected(self):
        """선정 완료 상태일 때 is_selected()가 True 반환"""
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
            status=CampaignStatus.SELECTED,
            created_at=datetime.now(),
            closed_at=datetime.now()
        )

        # Act
        result = campaign.is_selected()

        # Assert
        assert result is True

    def test_campaign_status_enum_has_required_values(self):
        """CampaignStatus Enum이 필요한 값들을 가지고 있는지 확인"""
        # Assert
        assert hasattr(CampaignStatus, 'RECRUITING')
        assert hasattr(CampaignStatus, 'CLOSED')
        assert hasattr(CampaignStatus, 'SELECTED')
        assert CampaignStatus.RECRUITING.value == 'RECRUITING'
        assert CampaignStatus.CLOSED.value == 'CLOSED'
        assert CampaignStatus.SELECTED.value == 'SELECTED'
