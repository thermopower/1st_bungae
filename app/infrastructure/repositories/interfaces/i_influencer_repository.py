"""
Influencer Repository 인터페이스
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.influencer import Influencer


class IInfluencerRepository(ABC):
    """인플루언서 리포지토리 인터페이스"""

    @abstractmethod
    def save(self, influencer: Influencer) -> Influencer:
        """
        인플루언서 정보 저장

        Args:
            influencer: Influencer 엔티티

        Returns:
            Influencer: 저장된 인플루언서 엔티티 (ID 포함)
        """
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Optional[Influencer]:
        """
        사용자 ID로 인플루언서 조회

        Args:
            user_id: 사용자 ID

        Returns:
            Optional[Influencer]: 인플루언서 엔티티 또는 None
        """
        pass

    @abstractmethod
    def find_by_id(self, influencer_id: int) -> Optional[Influencer]:
        """
        인플루언서 ID로 조회

        Args:
            influencer_id: 인플루언서 ID

        Returns:
            Optional[Influencer]: 인플루언서 엔티티 또는 None
        """
        pass

    @abstractmethod
    def exists_by_user_id(self, user_id: str) -> bool:
        """
        사용자 ID로 인플루언서 존재 여부 확인

        Args:
            user_id: 사용자 ID

        Returns:
            bool: 존재 여부
        """
        pass
