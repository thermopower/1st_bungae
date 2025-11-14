"""User Entity 테스트 (TDD)"""

import pytest
from datetime import datetime
from uuid import uuid4


class TestUserEntity:
    """User 도메인 엔티티 테스트"""

    def test_user_creation_with_valid_data(self):
        """정상 케이스: 유효한 데이터로 User 생성"""
        from app.domain.entities.user import User
        from app.domain.value_objects.email import Email

        user_id = str(uuid4())
        email = Email("test@example.com")
        created_at = datetime.utcnow()

        user = User(
            id=user_id,
            email=email,
            role=None,
            created_at=created_at
        )

        assert user.id == user_id
        assert user.email == email
        assert user.role is None
        assert user.created_at == created_at

    def test_user_has_role_returns_false_when_role_is_none(self):
        """비즈니스 로직: role이 None일 때 has_role()은 False 반환"""
        from app.domain.entities.user import User
        from app.domain.value_objects.email import Email

        user = User(
            id=str(uuid4()),
            email=Email("test@example.com"),
            role=None,
            created_at=datetime.utcnow()
        )

        assert user.has_role() is False

    def test_user_has_role_returns_true_when_role_is_advertiser(self):
        """비즈니스 로직: role이 'advertiser'일 때 has_role()은 True 반환"""
        from app.domain.entities.user import User
        from app.domain.value_objects.email import Email

        user = User(
            id=str(uuid4()),
            email=Email("test@example.com"),
            role="advertiser",
            created_at=datetime.utcnow()
        )

        assert user.has_role() is True

    def test_user_has_role_returns_true_when_role_is_influencer(self):
        """비즈니스 로직: role이 'influencer'일 때 has_role()은 True 반환"""
        from app.domain.entities.user import User
        from app.domain.value_objects.email import Email

        user = User(
            id=str(uuid4()),
            email=Email("test@example.com"),
            role="influencer",
            created_at=datetime.utcnow()
        )

        assert user.has_role() is True

    def test_user_equality(self):
        """동등성 테스트: 같은 ID를 가진 User는 동일"""
        from app.domain.entities.user import User
        from app.domain.value_objects.email import Email

        user_id = str(uuid4())
        user1 = User(
            id=user_id,
            email=Email("test1@example.com"),
            role=None,
            created_at=datetime.utcnow()
        )
        user2 = User(
            id=user_id,
            email=Email("test2@example.com"),
            role=None,
            created_at=datetime.utcnow()
        )
        user3 = User(
            id=str(uuid4()),
            email=Email("test1@example.com"),
            role=None,
            created_at=datetime.utcnow()
        )

        assert user1 == user2  # 같은 ID
        assert user1 != user3  # 다른 ID
