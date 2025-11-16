# app/infrastructure/repositories/interfaces/i_application_repository.py
"""
Application Repository Interface
체험단 지원 데이터 접근 계약
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.application import Application


class IApplicationRepository(ABC):
    """체험단 지원 Repository 인터페이스"""

    @abstractmethod
    def save(self, application: Application) -> Application:
        """
        지원 정보 저장

        Args:
            application: Application 엔티티

        Returns:
            저장된 Application 엔티티 (ID 포함)
        """
        pass

    @abstractmethod
    def find_by_campaign_id(self, campaign_id: int) -> List[Application]:
        """
        체험단의 지원자 목록 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            Application 엔티티 리스트
        """
        pass

    @abstractmethod
    def exists_by_campaign_and_influencer(
        self, campaign_id: int, influencer_id: int
    ) -> bool:
        """
        중복 지원 검증

        Args:
            campaign_id: 체험단 ID
            influencer_id: 인플루언서 ID

        Returns:
            이미 지원했으면 True, 아니면 False
        """
        pass

    @abstractmethod
    def update_status_bulk(
        self, application_ids: List[int], status: str
    ) -> None:
        """
        지원 상태 일괄 업데이트

        Args:
            application_ids: 업데이트할 지원 ID 리스트
            status: 변경할 상태
        """
        pass

    @abstractmethod
    def find_by_influencer_id(self, influencer_id: int) -> List[Application]:
        """
        인플루언서의 지원 내역 조회

        Args:
            influencer_id: 인플루언서 ID

        Returns:
            Application 엔티티 리스트 (지원일시 기준 최신순)
        """
        pass
