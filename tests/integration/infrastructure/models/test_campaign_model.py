# tests/integration/infrastructure/models/test_campaign_model.py
"""
Campaign Model 통합 테스트
실제 DB와 연동하여 ORM 동작 확인
"""

import pytest
from datetime import date, datetime
from app.infrastructure.persistence.models.campaign_model import CampaignModel
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel
from app.infrastructure.persistence.models.user_model import UserModel
from app.extensions import db


class TestCampaignModel:
    """Campaign ORM 모델 테스트"""

    @pytest.fixture(autouse=True)
    def setup_database(self, app):
        """각 테스트 전에 DB 초기화"""
        with app.app_context():
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()

    def test_campaign_model_creation(self, app):
        """Campaign 모델 생성 테스트"""
        with app.app_context():
            # Arrange: User 및 Advertiser 생성
            user = UserModel(
                id='test-user-id',
                email='test@example.com',
                role='advertiser'
            )
            db.session.add(user)
            db.session.flush()

            advertiser = AdvertiserModel(
                user_id=user.id,
                name='홍길동',
                birth_date=date(1990, 1, 1),
                phone_number='010-1234-5678',
                business_name='테스트 카페',
                address='서울시 강남구',
                business_phone='02-1234-5678',
                business_number='1234567890',
                representative_name='홍길동'
            )
            db.session.add(advertiser)
            db.session.flush()

            # Act: Campaign 생성
            campaign = CampaignModel(
                advertiser_id=advertiser.id,
                title='신메뉴 파스타 체험단 모집',
                description='새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
                quota=5,
                start_date=date(2025, 11, 15),
                end_date=date(2025, 11, 30),
                benefits='무료 식사 제공',
                conditions='인스타그램 피드 1개 + 스토리 2개 업로드',
                status='RECRUITING'
            )
            db.session.add(campaign)
            db.session.commit()

            # Assert
            saved_campaign = CampaignModel.query.filter_by(title='신메뉴 파스타 체험단 모집').first()
            assert saved_campaign is not None
            assert saved_campaign.advertiser_id == advertiser.id
            assert saved_campaign.quota == 5
            assert saved_campaign.status == 'RECRUITING'
            assert saved_campaign.image_url is None
            assert saved_campaign.closed_at is None

    def test_campaign_model_has_advertiser_relationship(self, app):
        """Campaign과 Advertiser 관계 확인"""
        with app.app_context():
            # Arrange: User, Advertiser, Campaign 생성
            user = UserModel(id='test-user-id', email='test@example.com', role='advertiser')
            db.session.add(user)
            db.session.flush()

            advertiser = AdvertiserModel(
                user_id=user.id,
                name='홍길동',
                birth_date=date(1990, 1, 1),
                phone_number='010-1234-5678',
                business_name='테스트 카페',
                address='서울시 강남구',
                business_phone='02-1234-5678',
                business_number='1234567890',
                representative_name='홍길동'
            )
            db.session.add(advertiser)
            db.session.flush()

            campaign = CampaignModel(
                advertiser_id=advertiser.id,
                title='테스트 체험단',
                description='설명',
                quota=5,
                start_date=date(2025, 11, 15),
                end_date=date(2025, 11, 30),
                benefits='혜택',
                conditions='조건',
                status='RECRUITING'
            )
            db.session.add(campaign)
            db.session.commit()

            # Act & Assert
            saved_campaign = CampaignModel.query.first()
            assert saved_campaign.advertiser is not None
            assert saved_campaign.advertiser.business_name == '테스트 카페'

    def test_campaign_model_tablename_is_campaign(self, app):
        """Campaign 테이블 이름 확인"""
        with app.app_context():
            # Assert
            assert CampaignModel.__tablename__ == 'campaign'
