"""
인플루언서 도메인 엔티티 단위 테스트
"""
import pytest
from datetime import date, datetime
from app.domain.entities.influencer import Influencer


class TestInfluencer:
    """Influencer 도메인 엔티티 테스트"""

    def test_create_influencer_with_valid_data(self):
        """유효한 데이터로 인플루언서 생성 테스트"""
        # Arrange
        user_id = "test-user-id"
        name = "홍길동"
        birth_date = date(1995, 5, 15)
        phone_number = "010-1234-5678"
        channel_name = "홍길동TV"
        channel_url = "https://www.youtube.com/@test"
        follower_count = 10000

        # Act
        influencer = Influencer(
            id=None,
            user_id=user_id,
            name=name,
            birth_date=birth_date,
            phone_number=phone_number,
            channel_name=channel_name,
            channel_url=channel_url,
            follower_count=follower_count,
            created_at=datetime.now()
        )

        # Assert
        assert influencer.user_id == user_id
        assert influencer.name == name
        assert influencer.birth_date == birth_date
        assert influencer.phone_number == phone_number
        assert influencer.channel_name == channel_name
        assert influencer.channel_url == channel_url
        assert influencer.follower_count == follower_count

    def test_create_influencer_with_zero_followers(self):
        """팔로워 수 0명으로 인플루언서 생성 테스트"""
        # Arrange
        follower_count = 0

        # Act
        influencer = Influencer(
            id=None,
            user_id="test-user-id",
            name="홍길동",
            birth_date=date(1995, 5, 15),
            phone_number="010-1234-5678",
            channel_name="홍길동TV",
            channel_url="https://www.youtube.com/@test",
            follower_count=follower_count,
            created_at=datetime.now()
        )

        # Assert
        assert influencer.follower_count == 0

    def test_influencer_equality(self):
        """인플루언서 객체 동등성 테스트"""
        # Arrange
        created_at = datetime.now()
        influencer1 = Influencer(
            id=1,
            user_id="test-user-id",
            name="홍길동",
            birth_date=date(1995, 5, 15),
            phone_number="010-1234-5678",
            channel_name="홍길동TV",
            channel_url="https://www.youtube.com/@test",
            follower_count=10000,
            created_at=created_at
        )
        influencer2 = Influencer(
            id=1,
            user_id="test-user-id",
            name="홍길동",
            birth_date=date(1995, 5, 15),
            phone_number="010-1234-5678",
            channel_name="홍길동TV",
            channel_url="https://www.youtube.com/@test",
            follower_count=10000,
            created_at=created_at
        )

        # Assert
        assert influencer1 == influencer2
