"""
체험단 상세 조회 E2E 테스트 (UC-012)
"""

import pytest
from flask import url_for
from datetime import date, timedelta
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel
from app.infrastructure.persistence.models.influencer_model import InfluencerModel
from app.infrastructure.persistence.models.campaign_model import CampaignModel
from app.extensions import db


class TestCampaignDetailRoutes:
    """체험단 상세 조회 라우트 테스트 (UC-012)"""

    @pytest.fixture
    def advertiser_user(self, app):
        """광고주 사용자 픽스처"""
        with app.app_context():
            user = UserModel(
                id='advertiser-id',
                email='advertiser@example.com',
                role='advertiser'
            )
            db.session.add(user)
            db.session.flush()

            advertiser = AdvertiserModel(
                id=1,
                user_id=user.id,
                name='홍길동',
                birth_date=date(1990, 1, 1),
                phone_number='010-1234-5678',
                business_name='테스트 카페',
                address='서울시 강남구 테헤란로 123',
                business_phone='02-1234-5678',
                business_number='1234567890',
                representative_name='홍길동'
            )
            db.session.add(advertiser)
            db.session.commit()
            yield user
            db.session.delete(advertiser)
            db.session.delete(user)
            db.session.commit()

    @pytest.fixture
    def influencer_user_without_info(self, app):
        """인플루언서 역할이지만 정보 미등록 사용자 픽스처"""
        with app.app_context():
            user = UserModel(
                id='influencer-no-info-id',
                email='influencer_no_info@example.com',
                role='influencer'
            )
            db.session.add(user)
            db.session.commit()
            yield user
            db.session.delete(user)
            db.session.commit()

    @pytest.fixture
    def influencer_user_with_info(self, app):
        """인플루언서 정보 등록된 사용자 픽스처"""
        with app.app_context():
            user = UserModel(
                id='influencer-with-info-id',
                email='influencer_with_info@example.com',
                role='influencer'
            )
            db.session.add(user)
            db.session.flush()

            influencer = InfluencerModel(
                id=1,
                user_id=user.id,
                name='테스트 인플루언서',
                birth_date=date(1995, 1, 1),
                phone_number='010-9876-5432',
                channel_name='test_influencer',
                channel_url='https://instagram.com/test_influencer',
                follower_count=10000
            )
            db.session.add(influencer)
            db.session.commit()
            yield user
            db.session.delete(influencer)
            db.session.delete(user)
            db.session.commit()

    @pytest.fixture
    def recruiting_campaign(self, app, advertiser_user):
        """모집 중인 체험단 픽스처"""
        with app.app_context():
            campaign = CampaignModel(
                id=1,
                advertiser_id=1,
                title='신메뉴 파스타 체험단 모집',
                description='새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
                quota=5,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=15),
                benefits='무료 식사 제공',
                conditions='인스타그램 피드 1개 + 스토리 2개 업로드',
                image_url=None,
                status='RECRUITING'
            )
            db.session.add(campaign)
            db.session.commit()
            yield campaign
            db.session.delete(campaign)
            db.session.commit()

    def test_campaign_detail_unauthenticated_user(self, client, app, recruiting_campaign):
        """
        TC 11.1: 미로그인 사용자 체험단 상세 조회
        - Given: 미로그인 사용자
        - When: 체험단 상세 페이지 접근
        - Then: 체험단 정보 표시, "로그인이 필요합니다" 메시지 + "로그인" 버튼
        """
        with app.test_request_context():
            # When: 체험단 상세 페이지 접근
            response = client.get(url_for('campaign.campaign_detail', campaign_id=1))

            # Then: 200 OK
            assert response.status_code == 200

            # Then: 체험단 정보 표시
            html = response.data.decode('utf-8')
            assert '신메뉴 파스타 체험단 모집' in html
            assert '테스트 카페' in html

            # Then: "로그인이 필요합니다" 메시지 표시
            assert '로그인이 필요합니다' in html

            # Then: "로그인" 버튼 표시
            assert '로그인' in html
            assert url_for('auth.login') in html

    def test_campaign_detail_influencer_without_info(
        self, client, app, recruiting_campaign, influencer_user_without_info
    ):
        """
        TC 11.7: 인플루언서 정보 미등록 사용자 체험단 상세 조회
        - Given: 로그인 상태지만 인플루언서 정보 미등록
        - When: 체험단 상세 페이지 접근
        - Then: 체험단 정보 표시, "인플루언서 정보를 먼저 등록해주세요" 메시지 + "정보 등록하기" 버튼
        """
        with app.test_request_context():
            # Given: 로그인 (세션 설정)
            with client.session_transaction() as sess:
                sess['user_id'] = influencer_user_without_info.id

            # When: 체험단 상세 페이지 접근
            response = client.get(url_for('campaign.campaign_detail', campaign_id=1))

            # Then: 200 OK
            assert response.status_code == 200

            # Then: 체험단 정보 표시
            html = response.data.decode('utf-8')
            assert '신메뉴 파스타 체험단 모집' in html

            # Then: "인플루언서 정보를 먼저 등록해주세요" 메시지 표시
            assert '인플루언서 정보를 먼저 등록해주세요' in html

            # Then: "정보 등록하기" 버튼 표시
            assert '정보 등록하기' in html
            assert url_for('influencer.register_influencer') in html

    def test_campaign_detail_advertiser_owner(
        self, client, app, recruiting_campaign, advertiser_user
    ):
        """
        TC 11.4: 광고주가 본인 체험단 조회
        - Given: 로그인된 광고주, 본인 체험단
        - When: 체험단 상세 페이지 접근
        - Then: 체험단 정보 표시, "관리하기" 버튼
        """
        with app.test_request_context():
            # Given: 로그인 (세션 설정)
            with client.session_transaction() as sess:
                sess['user_id'] = advertiser_user.id

            # When: 체험단 상세 페이지 접근
            response = client.get(url_for('campaign.campaign_detail', campaign_id=1))

            # Then: 200 OK
            assert response.status_code == 200

            # Then: 체험단 정보 표시
            html = response.data.decode('utf-8')
            assert '신메뉴 파스타 체험단 모집' in html

            # Then: "관리하기" 버튼 표시
            assert '관리하기' in html
            assert url_for('advertiser.campaign_detail', campaign_id=1) in html

            # Then: "지원하기" 버튼은 미표시 (지원하기 URL이 없어야 함)
            assert url_for('campaign.apply_campaign', campaign_id=1) not in html

    def test_campaign_detail_not_found(self, client, app):
        """
        TC 11.5: 체험단 없음 (404)
        - Given: 존재하지 않는 campaign_id
        - When: 체험단 상세 페이지 접근
        - Then: 404 페이지, "존재하지 않는 체험단입니다" 메시지
        """
        with app.test_request_context():
            # When: 존재하지 않는 체험단 ID로 접근
            response = client.get(url_for('campaign.campaign_detail', campaign_id=99999))

            # Then: 404 Not Found
            assert response.status_code == 404

    def test_campaign_detail_influencer_can_apply(
        self, client, app, recruiting_campaign, influencer_user_with_info
    ):
        """
        TC 11.2: 인플루언서가 지원 가능한 체험단 조회
        - Given: 로그인된 인플루언서, 모집 중인 체험단
        - When: 체험단 상세 페이지 접근
        - Then: 체험단 정보 표시, "지원하기" 버튼 (활성화)
        """
        with app.test_request_context():
            # Given: 로그인 (세션 설정)
            with client.session_transaction() as sess:
                sess['user_id'] = influencer_user_with_info.id

            # When: 체험단 상세 페이지 접근
            response = client.get(url_for('campaign.campaign_detail', campaign_id=1))

            # Then: 200 OK
            assert response.status_code == 200

            # Then: 체험단 정보 표시
            html = response.data.decode('utf-8')
            assert '신메뉴 파스타 체험단 모집' in html

            # Then: "지원하기" 버튼 표시 (활성화)
            assert '지원하기' in html
            assert url_for('campaign.apply_campaign', campaign_id=1) in html
