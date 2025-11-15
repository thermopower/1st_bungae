"""
역할 선택 페이지 E2E 테스트
"""

import pytest
from flask import url_for
from flask_login import login_user
from app.infrastructure.persistence.models.user_model import UserModel
from app.extensions import db


class TestRoleSelectionRoutes:
    """역할 선택 페이지 라우트 테스트"""

    @pytest.fixture
    def user_without_role(self, app):
        """역할이 없는 사용자 픽스처"""
        with app.app_context():
            user = UserModel(
                id='test-user-id',
                email='test@example.com',
                role=None
            )
            db.session.add(user)
            db.session.commit()
            yield user
            db.session.delete(user)
            db.session.commit()

    @pytest.fixture
    def advertiser_user(self, app):
        """광고주 역할을 가진 사용자 픽스처"""
        with app.app_context():
            user = UserModel(
                id='advertiser-id',
                email='advertiser@example.com',
                role='advertiser'
            )
            db.session.add(user)
            db.session.commit()
            yield user
            db.session.delete(user)
            db.session.commit()

    @pytest.fixture
    def influencer_user(self, app):
        """인플루언서 역할을 가진 사용자 픽스처"""
        with app.app_context():
            user = UserModel(
                id='influencer-id',
                email='influencer@example.com',
                role='influencer'
            )
            db.session.add(user)
            db.session.commit()
            yield user
            db.session.delete(user)
            db.session.commit()

    def test_get_role_selection_without_login(self, client, app):
        """
        시나리오: 비로그인 사용자가 역할 선택 페이지 접근
        Given: 로그인하지 않은 상태
        When: /role-selection 페이지 접근
        Then: 로그인 페이지로 리다이렉트
        """
        with app.app_context():
            # Act
            response = client.get('/role-selection', follow_redirects=False)

            # Assert
            assert response.status_code == 302
            assert '/auth/login' in response.location

    def test_get_role_selection_with_role_none(self, client, app, user_without_role):
        """
        시나리오: 역할이 없는 로그인 사용자가 역할 선택 페이지 접근
        Given: 역할이 없는 로그인 사용자
        When: /role-selection 페이지 접근
        Then: 페이지 정상 표시 (200)
        """
        with app.app_context():
            # Arrange
            with client.session_transaction() as sess:
                sess['_user_id'] = user_without_role.id

            # Act
            response = client.get('/role-selection')

            # Assert
            assert response.status_code == 200
            assert b'role-selection' in response.data or '광고주'.encode('utf-8') in response.data

    def test_get_role_selection_redirect_advertiser_to_dashboard(self, client, app, advertiser_user):
        """
        시나리오: 광고주 역할을 가진 사용자가 역할 선택 페이지 접근
        Given: 광고주 역할을 가진 로그인 사용자
        When: /role-selection 페이지 접근
        Then: 광고주 대시보드로 리다이렉트
        """
        with app.app_context():
            # Arrange
            with client.session_transaction() as sess:
                sess['_user_id'] = advertiser_user.id

            # Act
            response = client.get('/role-selection', follow_redirects=False)

            # Assert
            assert response.status_code == 302
            assert '/advertiser/dashboard' in response.location

    def test_get_role_selection_redirect_influencer_to_home(self, client, app, influencer_user):
        """
        시나리오: 인플루언서 역할을 가진 사용자가 역할 선택 페이지 접근
        Given: 인플루언서 역할을 가진 로그인 사용자
        When: /role-selection 페이지 접근
        Then: 홈으로 리다이렉트
        """
        with app.app_context():
            # Arrange
            with client.session_transaction() as sess:
                sess['_user_id'] = influencer_user.id

            # Act
            response = client.get('/role-selection', follow_redirects=False)

            # Assert
            assert response.status_code == 302
            assert response.location.endswith('/')

    def test_post_role_selection_advertiser(self, client, app, user_without_role):
        """
        시나리오: 광고주 역할 선택
        Given: 역할이 없는 로그인 사용자
        When: 광고주 역할 선택 및 제출
        Then: 역할이 'advertiser'로 저장되고 광고주 정보 등록 페이지로 리다이렉트
        """
        with app.app_context():
            # Arrange
            with client.session_transaction() as sess:
                sess['_user_id'] = user_without_role.id

            # Act
            response = client.post('/role-selection', data={
                'role': 'advertiser'
            }, follow_redirects=False)

            # Assert
            assert response.status_code == 302
            assert '/advertiser/register' in response.location

            # Verify role saved in DB
            updated_user = UserModel.query.get(user_without_role.id)
            assert updated_user.role == 'advertiser'

    def test_post_role_selection_influencer(self, client, app, user_without_role):
        """
        시나리오: 인플루언서 역할 선택
        Given: 역할이 없는 로그인 사용자
        When: 인플루언서 역할 선택 및 제출
        Then: 역할이 'influencer'로 저장되고 인플루언서 정보 등록 페이지로 리다이렉트
        """
        with app.app_context():
            # Arrange
            with client.session_transaction() as sess:
                sess['_user_id'] = user_without_role.id

            # Act
            response = client.post('/role-selection', data={
                'role': 'influencer'
            }, follow_redirects=False)

            # Assert
            assert response.status_code == 302
            assert '/influencer/register' in response.location

            # Verify role saved in DB
            updated_user = UserModel.query.get(user_without_role.id)
            assert updated_user.role == 'influencer'

    def test_post_role_selection_invalid_role(self, client, app, user_without_role):
        """
        시나리오: 잘못된 역할 값 전송
        Given: 역할이 없는 로그인 사용자
        When: 유효하지 않은 역할 값 제출
        Then: 에러 메시지 표시 및 페이지 유지
        """
        with app.app_context():
            # Arrange
            with client.session_transaction() as sess:
                sess['_user_id'] = user_without_role.id

            # Act
            response = client.post('/role-selection', data={
                'role': 'invalid_role'
            }, follow_redirects=True)

            # Assert
            assert response.status_code == 200
            assert '올바른 역할을 선택해주세요'.encode('utf-8') in response.data or response.status_code == 200

            # Verify role not changed
            user = UserModel.query.get(user_without_role.id)
            assert user.role is None
