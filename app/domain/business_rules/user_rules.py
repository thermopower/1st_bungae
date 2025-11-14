"""User Business Rules (사용자 비즈니스 규칙)"""

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.user import User


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

    @staticmethod
    def determine_redirect_url(user: 'User') -> str:
        """
        사용자 역할에 따른 리다이렉트 URL 결정

        Args:
            user: User 엔티티

        Returns:
            str: 리다이렉트 URL
                - 역할 없음: '/role-selection'
                - 광고주: '/advertiser/dashboard'
                - 인플루언서: '/'

        Raises:
            ValueError: 알 수 없는 역할
        """
        if not user.has_role():
            return '/role-selection'
        elif user.role == 'advertiser':
            return '/advertiser/dashboard'
        elif user.role == 'influencer':
            return '/'
        else:
            raise ValueError(f"Unknown role: {user.role}")
