"""Advertiser Business Rules (광고주 비즈니스 규칙)"""

from app.domain.entities.user import User


class AdvertiserRules:
    """광고주 비즈니스 규칙"""

    @staticmethod
    def can_register(user: User) -> bool:
        """
        광고주 등록 가능 여부 검증

        Args:
            user: 사용자 엔티티

        Returns:
            bool: 등록 가능하면 True, 아니면 False

        Business Rule:
            - 사용자가 역할(role)을 가지고 있지 않아야 함
            - 이미 광고주 또는 인플루언서로 등록된 경우 등록 불가
        """
        return not user.has_role()
