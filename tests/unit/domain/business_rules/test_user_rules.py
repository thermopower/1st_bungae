"""User Business Rules 테스트 (TDD)"""

import pytest


class TestUserRules:
    """User 비즈니스 규칙 테스트"""

    def test_validate_password_strength_with_valid_password(self):
        """정상 케이스: 영문+숫자 8자 이상 비밀번호"""
        from app.domain.business_rules.user_rules import UserRules

        # Given: 유효한 비밀번호
        password = "Password123"

        # When: 비밀번호 강도 검증
        result = UserRules.validate_password_strength(password)

        # Then: True 반환
        assert result is True

    def test_validate_password_strength_with_minimum_length(self):
        """경계 케이스: 최소 길이 8자"""
        from app.domain.business_rules.user_rules import UserRules

        password = "Pass123!"  # 정확히 8자

        result = UserRules.validate_password_strength(password)

        assert result is True

    def test_validate_password_strength_with_long_password(self):
        """경계 케이스: 긴 비밀번호"""
        from app.domain.business_rules.user_rules import UserRules

        password = "VeryLongPassword12345"  # 21자

        result = UserRules.validate_password_strength(password)

        assert result is True

    def test_validate_password_strength_fails_when_too_short(self):
        """에러 케이스: 7자 이하 비밀번호"""
        from app.domain.business_rules.user_rules import UserRules

        password = "Pass12"  # 6자

        result = UserRules.validate_password_strength(password)

        assert result is False

    def test_validate_password_strength_fails_when_no_letter(self):
        """에러 케이스: 영문 미포함"""
        from app.domain.business_rules.user_rules import UserRules

        password = "12345678"  # 숫자만

        result = UserRules.validate_password_strength(password)

        assert result is False

    def test_validate_password_strength_fails_when_no_digit(self):
        """에러 케이스: 숫자 미포함"""
        from app.domain.business_rules.user_rules import UserRules

        password = "Password"  # 영문만

        result = UserRules.validate_password_strength(password)

        assert result is False

    def test_validate_password_strength_with_special_characters(self):
        """추가 케이스: 특수문자 포함 (허용)"""
        from app.domain.business_rules.user_rules import UserRules

        password = "P@ssw0rd!"

        result = UserRules.validate_password_strength(password)

        assert result is True
