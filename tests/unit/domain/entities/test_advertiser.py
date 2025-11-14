"""Advertiser Entity 단위 테스트"""

import pytest
from datetime import datetime, date
from app.domain.entities.advertiser import Advertiser


class TestAdvertiserEntity:
    """Advertiser 엔티티 테스트"""

    def test_create_advertiser_with_valid_data(self):
        """유효한 데이터로 Advertiser 엔티티 생성"""
        # Arrange
        advertiser_data = {
            "id": None,
            "user_id": "test-uuid-1234",
            "name": "김광고",
            "birth_date": date(1985, 5, 15),
            "phone_number": "010-1234-5678",
            "business_name": "테스트 카페",
            "address": "서울시 강남구 테헤란로 123",
            "business_phone": "02-1234-5678",
            "business_number": "1234567890",
            "representative_name": "김대표",
            "created_at": datetime(2025, 11, 14, 10, 0, 0)
        }

        # Act
        advertiser = Advertiser(**advertiser_data)

        # Assert
        assert advertiser.user_id == "test-uuid-1234"
        assert advertiser.name == "김광고"
        assert advertiser.birth_date == date(1985, 5, 15)
        assert advertiser.phone_number == "010-1234-5678"
        assert advertiser.business_name == "테스트 카페"
        assert advertiser.address == "서울시 강남구 테헤란로 123"
        assert advertiser.business_phone == "02-1234-5678"
        assert advertiser.business_number == "1234567890"
        assert advertiser.representative_name == "김대표"
        assert advertiser.id is None

    def test_advertiser_equality_by_id(self):
        """Advertiser 동등성 검증 - ID가 같으면 동일"""
        # Arrange
        advertiser1 = Advertiser(
            id=1,
            user_id="test-uuid-1234",
            name="김광고",
            birth_date=date(1985, 5, 15),
            phone_number="010-1234-5678",
            business_name="테스트 카페",
            address="서울시 강남구 테헤란로 123",
            business_phone="02-1234-5678",
            business_number="1234567890",
            representative_name="김대표",
            created_at=datetime(2025, 11, 14, 10, 0, 0)
        )

        advertiser2 = Advertiser(
            id=1,
            user_id="different-uuid",
            name="다른이름",
            birth_date=date(1990, 1, 1),
            phone_number="010-9999-9999",
            business_name="다른 카페",
            address="서울시 서초구",
            business_phone="02-9999-9999",
            business_number="9999999999",
            representative_name="다른대표",
            created_at=datetime(2025, 11, 14, 11, 0, 0)
        )

        # Act & Assert
        assert advertiser1 == advertiser2  # ID만 같으면 동일

    def test_advertiser_inequality_by_different_id(self):
        """Advertiser 동등성 검증 - ID가 다르면 다름"""
        # Arrange
        advertiser1 = Advertiser(
            id=1,
            user_id="test-uuid-1234",
            name="김광고",
            birth_date=date(1985, 5, 15),
            phone_number="010-1234-5678",
            business_name="테스트 카페",
            address="서울시 강남구 테헤란로 123",
            business_phone="02-1234-5678",
            business_number="1234567890",
            representative_name="김대표",
            created_at=datetime(2025, 11, 14, 10, 0, 0)
        )

        advertiser2 = Advertiser(
            id=2,
            user_id="test-uuid-1234",
            name="김광고",
            birth_date=date(1985, 5, 15),
            phone_number="010-1234-5678",
            business_name="테스트 카페",
            address="서울시 강남구 테헤란로 123",
            business_phone="02-1234-5678",
            business_number="1234567890",
            representative_name="김대표",
            created_at=datetime(2025, 11, 14, 10, 0, 0)
        )

        # Act & Assert
        assert advertiser1 != advertiser2  # ID가 다르면 다름
