"""
인플루언서 비즈니스 규칙
"""
from app.domain.entities.user import User


class InfluencerRules:
    """인플루언서 관련 비즈니스 규칙"""

    @staticmethod
    def can_register(user: User) -> bool:
        """
        인플루언서 등록 가능 여부 검증

        Args:
            user: 사용자 엔티티

        Returns:
            bool: 등록 가능 여부
        """
        return not user.has_role()

    @staticmethod
    def validate_follower_count(follower_count: int) -> bool:
        """
        팔로워 수 검증

        Args:
            follower_count: 팔로워 수

        Returns:
            bool: 유효성 여부
        """
        return follower_count >= 0
