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
