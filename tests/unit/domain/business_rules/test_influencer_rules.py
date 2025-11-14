"""
인플루언서 비즈니스 규칙 단위 테스트
"""
import pytest
from app.domain.business_rules.influencer_rules import InfluencerRules
from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from datetime import datetime


class TestInfluencerRules:
    """InfluencerRules 비즈니스 규칙 테스트"""

    def test_can_register_when_user_has_no_role(self):
        """역할이 없는 사용자는 인플루언서 등록 가능"""
        # Arrange
        user = User(
            id="test-user-id",
            email=Email("test@example.com"),
            role=None,
            created_at=datetime.now()
        )

        # Act
        result = InfluencerRules.can_register(user)

        # Assert
        assert result is True

    def test_cannot_register_when_user_is_advertiser(self):
        """광고주 역할을 가진 사용자는 인플루언서 등록 불가"""
        # Arrange
        user = User(
            id="test-user-id",
            email=Email("test@example.com"),
            role="advertiser",
            created_at=datetime.now()
        )

        # Act
        result = InfluencerRules.can_register(user)

        # Assert
        assert result is False

    def test_cannot_register_when_user_is_already_influencer(self):
        """이미 인플루언서 역할을 가진 사용자는 재등록 불가"""
        # Arrange
        user = User(
            id="test-user-id",
            email=Email("test@example.com"),
            role="influencer",
            created_at=datetime.now()
        )

        # Act
        result = InfluencerRules.can_register(user)

        # Assert
        assert result is False

    def test_validate_follower_count_with_zero(self):
        """팔로워 수 0은 유효함"""
        # Act
        result = InfluencerRules.validate_follower_count(0)

        # Assert
        assert result is True

    def test_validate_follower_count_with_positive_number(self):
        """양수 팔로워 수는 유효함"""
        # Act
        result = InfluencerRules.validate_follower_count(10000)

        # Assert
        assert result is True

    def test_validate_follower_count_with_negative_number(self):
        """음수 팔로워 수는 무효함"""
        # Act
        result = InfluencerRules.validate_follower_count(-1)

        # Assert
        assert result is False
