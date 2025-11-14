"""User Business Rules (사용자 비즈니스 규칙)"""

import re


class UserRules:
    """사용자 관련 비즈니스 규칙"""

    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        비밀번호 강도 검증

        규칙:
        - 최소 8자 이상
        - 영문 포함 필수
        - 숫자 포함 필수

        Args:
            password: 검증할 비밀번호

        Returns:
            bool: 유효하면 True, 아니면 False
        """
        # 최소 길이 검증
        if len(password) < 8:
            return False

        # 영문 포함 검증
        if not re.search(r'[A-Za-z]', password):
            return False

        # 숫자 포함 검증
        if not re.search(r'\d', password):
            return False

        return True
