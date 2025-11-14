"""Advertiser Business Rules 단위 테스트"""

import pytest
from datetime import datetime
from app.domain.entities.user import User
from app.domain.entities.advertiser import Advertiser
from app.domain.business_rules.advertiser_rules import AdvertiserRules
from app.domain.value_objects.email import Email
from datetime import date


class TestAdvertiserRules:
    """광고주 비즈니스 규칙 테스트"""

    def test_can_register_returns_true_when_user_has_no_role(self):
        """역할이 없는 사용자는 광고주로 등록 가능"""
        # Arrange
        user = User(
            id="test-uuid",
            email=Email("test@example.com"),
            role=None,
            created_at=datetime.now()
        )

        # Act
        result = AdvertiserRules.can_register(user)

        # Assert
        assert result is True

    def test_can_register_returns_false_when_user_already_has_advertiser_role(self):
        """이미 광고주 역할이 있는 사용자는 등록 불가"""
        # Arrange
        user = User(
            id="test-uuid",
            email=Email("test@example.com"),
            role="advertiser",
            created_at=datetime.now()
        )

        # Act
        result = AdvertiserRules.can_register(user)

        # Assert
        assert result is False

    def test_can_register_returns_false_when_user_already_has_influencer_role(self):
        """이미 인플루언서 역할이 있는 사용자는 등록 불가"""
        # Arrange
        user = User(
            id="test-uuid",
            email=Email("test@example.com"),
            role="influencer",
            created_at=datetime.now()
        )

        # Act
        result = AdvertiserRules.can_register(user)

        # Assert
        assert result is False
