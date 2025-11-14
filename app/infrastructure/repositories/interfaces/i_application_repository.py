# app/infrastructure/repositories/interfaces/i_application_repository.py
"""
Application Repository Interface
체험단 지원 데이터 접근 계약
"""

from abc import ABC, abstractmethod
from typing import Optional


class IApplicationRepository(ABC):
    """체험단 지원 Repository 인터페이스"""

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
