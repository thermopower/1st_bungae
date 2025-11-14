"""Advertiser Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.advertiser import Advertiser


class IAdvertiserRepository(ABC):
    """광고주 저장소 인터페이스"""

    @abstractmethod
    def save(self, advertiser: Advertiser) -> Advertiser:
        """
        광고주 정보 저장

        Args:
            advertiser: 광고주 엔티티

        Returns:
            Advertiser: 저장된 광고주 엔티티 (ID 포함)
        """
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Optional[Advertiser]:
        """
        사용자 ID로 광고주 조회

        Args:
            user_id: 사용자 ID (UUID)

        Returns:
            Optional[Advertiser]: 광고주 엔티티 (없으면 None)
        """
        pass

    @abstractmethod
    def exists_by_business_number(self, business_number: str) -> bool:
        """
        사업자등록번호 중복 검증

        Args:
            business_number: 사업자등록번호 (10자리)

        Returns:
            bool: 존재하면 True, 아니면 False
        """
        pass

    @abstractmethod
    def find_by_id(self, advertiser_id: int) -> Optional[Advertiser]:
        """
        광고주 ID로 조회

        Args:
            advertiser_id: 광고주 ID

        Returns:
            Optional[Advertiser]: 광고주 엔티티 (없으면 None)
        """
        pass
