"""User Rules 테스트 - 로그인 관련"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from datetime import datetime, UTC
import pytest

# Flask 없이 도메인 모듈만 import
from app.domain.entities.user import User as DomainUser
from app.domain.value_objects.email import Email
from app.domain.business_rules.user_rules import UserRules


class TestDetermineRedirectUrl:
    """determine_redirect_url 메서드 테스트"""

    def test_redirect_to_role_selection_when_no_role(self):
        """역할이 없는 사용자는 역할 선택 페이지로 리다이렉트"""
        # Arrange: 역할이 없는 사용자
        user = DomainUser(
            id="test-user-id",
            email=Email("test@example.com"),
            role=None,
            created_at=datetime.now(UTC)
        )

        # Act: determine_redirect_url 호출
        redirect_url = UserRules.determine_redirect_url(user)

        # Assert: '/role-selection' 반환
        assert redirect_url == '/role-selection'

    def test_redirect_to_advertiser_dashboard_when_advertiser(self):
        """광고주 역할을 가진 사용자는 광고주 대시보드로 리다이렉트"""
        # Arrange: 광고주 역할을 가진 사용자
        user = DomainUser(
            id="test-user-id",
            email=Email("advertiser@example.com"),
            role='advertiser',
            created_at=datetime.now(UTC)
        )

        # Act: determine_redirect_url 호출
        redirect_url = UserRules.determine_redirect_url(user)

        # Assert: '/advertiser/dashboard' 반환
        assert redirect_url == '/advertiser/dashboard'

    def test_redirect_to_home_when_influencer(self):
        """인플루언서 역할을 가진 사용자는 홈으로 리다이렉트"""
        # Arrange: 인플루언서 역할을 가진 사용자
        user = DomainUser(
            id="test-user-id",
            email=Email("influencer@example.com"),
            role='influencer',
            created_at=datetime.now(UTC)
        )

        # Act: determine_redirect_url 호출
        redirect_url = UserRules.determine_redirect_url(user)

        # Assert: '/' 반환
        assert redirect_url == '/'

    def test_raise_value_error_when_unknown_role(self):
        """알 수 없는 역할이면 ValueError 발생"""
        # Arrange: 알 수 없는 역할을 가진 사용자
        user = DomainUser(
            id="test-user-id",
            email=Email("test@example.com"),
            role='admin',  # 지원하지 않는 역할
            created_at=datetime.now(UTC)
        )

        # Act & Assert: ValueError 발생
        with pytest.raises(ValueError) as exc_info:
            UserRules.determine_redirect_url(user)

        assert "Unknown role" in str(exc_info.value)
