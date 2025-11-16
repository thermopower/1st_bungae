# -*- coding: utf-8 -*-
"""
인플루언서 라우트 트랜잭션 처리 통합 테스트
"""

import pytest
from datetime import date
from flask import url_for
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.models.influencer_model import InfluencerModel
from app.extensions import db
from tests.conftest import login_user, count_records


class TestInfluencerRegisterTransaction:
    """인플루언서 정보 등록 트랜잭션 테스트"""

    def test_register_influencer_success(self, client, app, influencer_user):
        """TC-RI-001: 정상 케이스 - 인플루언서 정보 등록 성공 및 DB 커밋 검증"""
        with app.app_context():
            # Arrange: 테스트 데이터 준비
            login_user(client, influencer_user.id)
            form_data = {
                'name': '김인플루',
                'birth_date': '1995-03-15',
                'phone_number': '010-9876-5432',
                'channel_type': 'instagram',
                'channel_name': 'test_influencer',
                'channel_url': 'https://instagram.com/test_influencer',
                'follower_count': 10000
            }

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(InfluencerModel)
            assert before_count == 0

            # Act: 인플루언서 정보 등록 요청
            response = client.post(
                '/influencer/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답
            assert response.status_code == 302
            assert response.location == '/' or '/main' in response.location or response.location.endswith('/')

            # Assert - DB 저장 확인
            after_count = count_records(InfluencerModel)
            assert after_count == 1

            # Assert - 저장된 데이터 검증
            influencer = db.session.query(InfluencerModel).filter_by(
                user_id=influencer_user.id
            ).first()
            assert influencer is not None
            assert influencer.name == '김인플루'
            assert influencer.follower_count == 10000

            # Assert - Flash 메시지
            with client.session_transaction() as sess:
                flashes = sess.get('_flashes', [])
                assert len(flashes) == 1
                assert flashes[0][0] == 'success'
                assert '성공적으로 등록되었습니다' in flashes[0][1]

    def test_register_influencer_duplicate_rollback(self, client, app, monkeypatch):
        """TC-RI-002: 예외 케이스 - 중복 등록 시 롤백 검증"""
        with app.app_context():
            # Arrange: 이미 등록된 인플루언서 생성
            user = UserModel(
                id='registered-influencer-id',
                email='registered_influencer@example.com',
                role='influencer'
            )
            db.session.add(user)
            db.session.flush()

            influencer = InfluencerModel(
                id=1,
                user_id=user.id,
                name='기존 인플루언서',
                birth_date=date(1995, 1, 1),
                phone_number='010-1111-2222',
                channel_name='existing_channel',
                channel_url='https://instagram.com/existing',
                follower_count=5000
            )
            db.session.add(influencer)
            db.session.commit()

            login_user(client, user.id)
            form_data = {
                'name': '새로운 이름',
                'birth_date': '1998-08-08',
                'phone_number': '010-9999-9999',
                'channel_type': 'instagram',
                'channel_name': 'new_channel',
                'channel_url': 'https://instagram.com/new',
                'follower_count': 20000
            }

            # Mock: render_template을 모킹하여 템플릿 렌더링 건너뛰기
            from flask import Response
            def mock_render_template(*args, **kwargs):
                return Response("Mocked template", status=200)

            monkeypatch.setattr('app.presentation.routes.influencer_routes.render_template', mock_render_template)

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(InfluencerModel)
            assert before_count == 1

            # Act: 중복 등록 시도
            response = client.post(
                '/influencer/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답 (폼 재표시)
            assert response.status_code == 200

            # Assert - DB 롤백 확인 (레코드 개수 변화 없음)
            after_count = count_records(InfluencerModel)
            assert after_count == 1

            # Assert - 기존 데이터 유지 확인
            influencer = db.session.query(InfluencerModel).filter_by(
                user_id=user.id
            ).first()
            assert influencer.name == '기존 인플루언서'

            # Assert - Flash 메시지 확인 (세션에서 직접 확인)
            with client.session_transaction() as sess:
                flashes = sess.get('_flashes', [])
                if flashes:
                    messages = [msg[1] for msg in flashes]
                    assert any('인플루언서' in msg or 'influencer' in msg.lower() for msg in messages)

    def test_register_influencer_invalid_value_rollback(
        self, client, app, influencer_user, monkeypatch
    ):
        """TC-RI-003: 예외 케이스 - 잘못된 값 입력 시 롤백 검증"""
        with app.app_context():
            # Arrange: 테스트 데이터 준비
            login_user(client, influencer_user.id)
            form_data = {
                'name': '김인플루',
                'birth_date': '1995-03-15',
                'phone_number': '010-9876-5432',
                'channel_type': 'instagram',
                'channel_name': 'test_influencer',
                'channel_url': 'https://instagram.com/test_influencer',
                'follower_count': 10000
            }

            # Mock: render_template을 모킹하여 템플릿 렌더링 건너뛰기
            from flask import Response
            def mock_render_template(*args, **kwargs):
                return Response("Mocked template", status=200)

            monkeypatch.setattr('app.presentation.routes.influencer_routes.render_template', mock_render_template)

            # Mock: influencer_service.register_influencer()에서 ValueError 발생
            from app.application.services.influencer_service import InfluencerService

            def mock_register_influencer(*args, **kwargs):
                raise ValueError("팔로워 수는 0 이상이어야 합니다.")

            monkeypatch.setattr(
                InfluencerService,
                'register_influencer',
                mock_register_influencer
            )

            # DB 레코드 개수 확인 (Before)
            before_count = count_records(InfluencerModel)

            # Act: 등록 시도 (예외 발생 시뮬레이션)
            response = client.post(
                '/influencer/register',
                data=form_data,
                follow_redirects=False
            )

            # Assert - HTTP 응답 (폼 재표시)
            assert response.status_code == 200

            # Assert - DB 롤백 확인
            after_count = count_records(InfluencerModel)
            assert after_count == before_count

            # Assert - Flash 메시지 확인
            with client.session_transaction() as sess:
                flashes = sess.get('_flashes', [])
                if flashes:
                    messages = [msg[1] for msg in flashes]
                    assert any('팔로워' in msg or 'ValueError' in str(msg) for msg in messages)
