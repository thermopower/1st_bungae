# tests/conftest.py
"""
Pytest 설정 및 공통 픽스처
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 테스트용 환경 변수 설정
os.environ['SUPABASE_URL'] = 'https://eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlc3QiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYwOTQ1OTIwMCwiZXhwIjoxOTI1MDM1MjAwfQ.test'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlc3QiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYwOTQ1OTIwMCwiZXhwIjoxOTI1MDM1MjAwfQ.test-key-test-key-test-key-test-key-test'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

# Supabase Client Mock (모듈 임포트 전에 Mock 설정)
mock_supabase_client = MagicMock()
sys.modules['supabase'] = MagicMock()
sys.modules['supabase._sync'] = MagicMock()
sys.modules['supabase._sync.client'] = MagicMock()

from app.config import Config


class TestConfig(Config):
    """테스트용 설정"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='function')
def app():
    """Flask 앱 픽스처 (함수 범위)"""
    app = create_app(TestConfig)

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Flask 테스트 클라이언트"""
    return app.test_client()


# ============================================================
# 통합 테스트용 사용자 픽스처
# ============================================================

@pytest.fixture
def advertiser_user(app):
    """광고주 사용자 픽스처 (정보 미등록)"""
    from app.infrastructure.persistence.models.user_model import UserModel

    with app.app_context():
        user = UserModel(
            id='advertiser-id',
            email='advertiser@example.com',
            role='advertiser'
        )
        _db.session.add(user)
        _db.session.commit()
        yield user


@pytest.fixture
def influencer_user(app):
    """인플루언서 사용자 픽스처 (정보 미등록)"""
    from app.infrastructure.persistence.models.user_model import UserModel

    with app.app_context():
        user = UserModel(
            id='influencer-id',
            email='influencer@example.com',
            role='influencer'
        )
        _db.session.add(user)
        _db.session.commit()
        yield user


@pytest.fixture
def registered_advertiser(app):
    """광고주 정보 등록된 사용자 픽스처"""
    from datetime import date
    from app.infrastructure.persistence.models.user_model import UserModel
    from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel

    with app.app_context():
        user = UserModel(
            id='registered-advertiser-id',
            email='registered_advertiser@example.com',
            role='advertiser'
        )
        _db.session.add(user)
        _db.session.flush()

        advertiser = AdvertiserModel(
            id=1,
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
        _db.session.add(advertiser)
        _db.session.commit()
        yield user


# ============================================================
# 헬퍼 함수
# ============================================================

def login_user(client, user_id):
    """테스트용 로그인 헬퍼 (Flask-Login 호환)"""
    with client.session_transaction() as sess:
        sess['_user_id'] = user_id
        sess['_fresh'] = True


def count_records(model):
    """DB 레코드 개수 조회"""
    return _db.session.query(model).count()
