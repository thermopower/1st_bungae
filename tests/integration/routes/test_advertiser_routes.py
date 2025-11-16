# -*- coding: utf-8 -*-
"""
광고주 라우트 트랜잭션 처리 통합 테스트
"""

import pytest
from datetime import date
from flask import url_for
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel
from app.infrastructure.persistence.models.campaign_model import CampaignModel
from app.extensions import db
from tests.conftest import login_user, count_records


class TestAdvertiserRegisterTransaction:
    """광고주 정보 등록 트랜잭션 테스트"""

    def test_register_advertiser_success(self, client, app, advertiser_user):
        """TC-RA-001: 정상 케이스 - 광고주 정보 등록 성공 및 DB 커밋 검증"""
        with app.app_context():
            # Arrange: 테스트 데이터 준비
            login_user(client, advertiser_user.id)
            form_data = {
                'name': '홍길동',
                'birth_date': '1990-01-01',
                'phone_number': '010-1234-5678',
                'business_name': '테스트 카페',
                'address': '서울시 강남구 테헤란로 123',
                'business_phone': '02-1234-5678',
                'business_number': '123-45-67890',
                'representative_name': '홍길동'
            }

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(AdvertiserModel)
            assert before_count == 0

            # Act: 광고주 정보 등록 요청
            response = client.post(
                '/advertiser/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답
            assert response.status_code == 302
            assert '/advertiser/dashboard' in response.location

            # Assert - DB 저장 확인
            after_count = count_records(AdvertiserModel)
            assert after_count == 1

            # Assert - 저장된 데이터 검증
            advertiser = db.session.query(AdvertiserModel).filter_by(
                user_id=advertiser_user.id
            ).first()
            assert advertiser is not None
            assert advertiser.name == '홍길동'
            assert advertiser.business_number == '1234567890'  # 하이픈 제거됨

            # Assert - Flash 메시지
            with client.session_transaction() as sess:
                flashes = sess.get('_flashes', [])
                assert len(flashes) == 1
                assert flashes[0][0] == 'success'
                assert '성공적으로 등록되었습니다' in flashes[0][1]

    def test_register_advertiser_duplicate_rollback(self, client, app, registered_advertiser):
        """TC-RA-002: 예외 케이스 - 중복 등록 시 롤백 검증"""
        with app.app_context():
            # Arrange: 이미 등록된 사용자로 로그인
            login_user(client, registered_advertiser.id)
            form_data = {
                'name': '김철수',
                'birth_date': '1985-05-05',
                'phone_number': '010-9999-8888',
                'business_name': '새로운 카페',
                'address': '부산시',
                'business_phone': '051-1111-2222',
                'business_number': '999-88-77777',
                'representative_name': '김철수'
            }

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(AdvertiserModel)
            assert before_count == 1

            # Act: 중복 등록 시도
            response = client.post(
                '/advertiser/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답 (폼 재표시)
            assert response.status_code == 200

            # Assert - DB 롤백 확인 (레코드 개수 변화 없음)
            after_count = count_records(AdvertiserModel)
            assert after_count == 1

            # Assert - 기존 데이터 유지 확인
            advertiser = db.session.query(AdvertiserModel).filter_by(
                user_id=registered_advertiser.id
            ).first()
            assert advertiser.name == '홍길동'  # 기존 이름 유지

            # Assert - Flash 메시지
            html = response.data.decode('utf-8')
            assert '이미 광고주 정보가 등록되어 있습니다' in html or \
                   'AdvertiserAlreadyRegisteredException' in str(response.data)

    def test_register_advertiser_duplicate_business_number_rollback(
        self, client, app, registered_advertiser, advertiser_user
    ):
        """TC-RA-003: 예외 케이스 - 사업자번호 중복 시 롤백 검증"""
        with app.app_context():
            # Arrange: advertiser_user는 미등록 상태
            login_user(client, advertiser_user.id)
            form_data = {
                'name': '김철수',
                'birth_date': '1985-05-05',
                'phone_number': '010-9999-8888',
                'business_name': '새로운 카페',
                'address': '부산시',
                'business_phone': '051-1111-2222',
                'business_number': '123-45-67890',  # 기존 사용자와 동일 (하이픈 포함)
                'representative_name': '김철수'
            }

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(AdvertiserModel)
            assert before_count == 1

            # Act: 동일한 사업자번호로 등록 시도
            response = client.post(
                '/advertiser/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답
            assert response.status_code == 200

            # Assert - DB 롤백 확인 (레코드 개수 변화 없음)
            after_count = count_records(AdvertiserModel)
            assert after_count == 1

            # Assert - advertiser_user는 등록되지 않음
            advertiser = db.session.query(AdvertiserModel).filter_by(
                user_id=advertiser_user.id
            ).first()
            assert advertiser is None

            # Assert - Flash 메시지
            html = response.data.decode('utf-8')
            assert '사업자등록번호' in html or 'BusinessNumberAlreadyExistsException' in str(response.data)

    def test_register_advertiser_general_exception_rollback(
        self, client, app, advertiser_user, monkeypatch
    ):
        """TC-RA-004: 예외 케이스 - 일반 예외 발생 시 롤백 검증"""
        with app.app_context():
            # Arrange: 테스트 데이터 준비
            login_user(client, advertiser_user.id)
            form_data = {
                'name': '홍길동',
                'birth_date': '1990-01-01',
                'phone_number': '010-1234-5678',
                'business_name': '테스트 카페',
                'address': '서울시 강남구 테헤란로 123',
                'business_phone': '02-1234-5678',
                'business_number': '123-45-67890',
                'representative_name': '홍길동'
            }

            # Mock: advertiser_service.register_advertiser()에서 예외 발생
            from app.application.services.advertiser_service import AdvertiserService

            def mock_register_advertiser(*args, **kwargs):
                raise Exception("데이터베이스 연결 오류")

            monkeypatch.setattr(
                AdvertiserService,
                'register_advertiser',
                mock_register_advertiser
            )

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(AdvertiserModel)

            # Act: 등록 시도 (예외 발생 시뮬레이션)
            response = client.post(
                '/advertiser/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답
            assert response.status_code == 200

            # Assert - DB 롤백 확인
            after_count = count_records(AdvertiserModel)
            assert after_count == before_count

            # Assert - Flash 메시지
            html = response.data.decode('utf-8')
            assert '오류가 발생했습니다' in html


class TestCampaignCreateTransaction:
    """체험단 생성 트랜잭션 테스트"""

    def test_create_campaign_success(self, client, app, registered_advertiser):
        """TC-CC-001: 정상 케이스 - 체험단 생성 성공 및 DB 커밋 검증"""
        with app.app_context():
            # Arrange: 테스트 데이터 준비
            login_user(client, registered_advertiser.id)
            form_data = {
                'title': '신메뉴 파스타 체험단 모집',
                'description': '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
                'quota': 5,
                'start_date': '2025-11-16',
                'end_date': '2025-12-01',
                'benefits': '무료 식사 제공',
                'conditions': '인스타그램 피드 1개 + 스토리 2개 업로드'
            }

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(CampaignModel)
            assert before_count == 0

            # Act: 체험단 생성 요청
            response = client.post(
                '/advertiser/campaign/create',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답
            assert response.status_code == 302
            assert '/advertiser/dashboard' in response.location

            # Assert - DB 저장 확인
            after_count = count_records(CampaignModel)
            assert after_count == 1

            # Assert - 저장된 데이터 검증
            campaign = db.session.query(CampaignModel).filter_by(
                title='신메뉴 파스타 체험단 모집'
            ).first()
            assert campaign is not None
            assert campaign.quota == 5
            assert campaign.status == 'RECRUITING'
            assert campaign.advertiser_id == 1

            # Assert - Flash 메시지
            with client.session_transaction() as sess:
                flashes = sess.get('_flashes', [])
                assert len(flashes) == 1
                assert flashes[0][0] == 'success'
                assert '성공적으로 생성되었습니다' in flashes[0][1]

    def test_create_campaign_form_validation_failure(self, client, app, registered_advertiser):
        """TC-CC-002: 폼 검증 실패 - 필수 필드 누락 시 Flash 메시지 및 DB 저장 안 됨"""
        with app.app_context():
            # Arrange: 필수 필드 누락된 폼 데이터
            login_user(client, registered_advertiser.id)
            form_data = {
                'description': '설명',
                'quota': 5,
                'start_date': '2025-11-16',
                'end_date': '2025-12-01',
                'benefits': '혜택',
                'conditions': '조건'
                # title 누락
            }

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(CampaignModel)

            # Act: 체험단 생성 시도 (필수 필드 누락)
            response = client.post(
                '/advertiser/campaign/create',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답 (폼 재표시)
            assert response.status_code == 200

            # Assert - DB 저장 안 됨
            after_count = count_records(CampaignModel)
            assert after_count == before_count

            # Assert - Flash 메시지 (폼 에러)
            html = response.data.decode('utf-8')
            assert 'title' in html.lower() or 'This field is required' in html

    def test_create_campaign_general_exception_rollback(
        self, client, app, registered_advertiser, monkeypatch
    ):
        """TC-CC-003: 예외 케이스 - 일반 예외 발생 시 롤백 검증"""
        with app.app_context():
            # Arrange: 테스트 데이터 준비
            login_user(client, registered_advertiser.id)
            form_data = {
                'title': '신메뉴 파스타 체험단 모집',
                'description': '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
                'quota': 5,
                'start_date': '2025-11-16',
                'end_date': '2025-12-01',
                'benefits': '무료 식사 제공',
                'conditions': '인스타그램 피드 1개 + 스토리 2개 업로드'
            }

            # Mock: campaign_service.create_campaign()에서 예외 발생
            from app.application.services.campaign_service import CampaignService

            def mock_create_campaign(*args, **kwargs):
                raise Exception("데이터베이스 연결 오류")

            monkeypatch.setattr(
                CampaignService,
                'create_campaign',
                mock_create_campaign
            )

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(CampaignModel)

            # Act: 체험단 생성 시도 (예외 발생 시뮬레이션)
            response = client.post(
                '/advertiser/campaign/create',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답
            assert response.status_code == 200

            # Assert - DB 롤백 확인
            after_count = count_records(CampaignModel)
            assert after_count == before_count

            # Assert - Flash 메시지
            html = response.data.decode('utf-8')
            assert '오류가 발생했습니다' in html
