# app/infrastructure/repositories/interfaces/i_campaign_repository.py
"""
Campaign Repository Interface
체험단 데이터 접근 계약
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.campaign import Campaign


class ICampaignRepository(ABC):
    """체험단 Repository 인터페이스"""

    @abstractmethod
    def find_by_id(self, campaign_id: int) -> Optional[Campaign]:
        """
        체험단 ID로 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            Campaign 엔티티 또는 None
        """
        pass

    @abstractmethod
    def find_by_id_with_advertiser(self, campaign_id: int) -> Optional[tuple]:
        """
        체험단 ID로 광고주 정보 포함하여 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            (Campaign, business_name, business_address) 튜플 또는 None
        """
        pass

    @abstractmethod
    def get_application_count(self, campaign_id: int) -> int:
        """
        지원자 수 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            지원자 수
        """
        pass

    @abstractmethod
    def find_recruiting_campaigns(
        self, skip: int = 0, limit: int = 12, sort: str = 'latest'
    ) -> List[tuple]:
        """
        모집 중인 체험단 목록 조회

        Args:
            skip: 건너뛸 레코드 수
            limit: 조회할 레코드 수
            sort: 정렬 기준 ('latest', 'deadline', 'popular')

        Returns:
            (Campaign, business_name, application_count) 튜플 리스트
        """
        pass

    @abstractmethod
    def count_recruiting_campaigns(self) -> int:
        """
        모집 중인 체험단 총 개수 조회

        Returns:
            총 개수
        """
        pass

    @abstractmethod
    def save(self, campaign: Campaign) -> Campaign:
        """
        체험단 저장

        Args:
            campaign: Campaign 엔티티

        Returns:
            저장된 Campaign 엔티티 (ID 포함)
        """
        pass
