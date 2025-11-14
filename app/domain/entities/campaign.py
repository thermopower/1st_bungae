# app/domain/entities/campaign.py
"""
Campaign 도메인 엔티티
체험단 비즈니스 객체
"""

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional


class CampaignStatus(Enum):
    """체험단 상태 Enum"""
    RECRUITING = 'RECRUITING'  # 모집 중
    CLOSED = 'CLOSED'  # 모집 종료
    SELECTED = 'SELECTED'  # 선정 완료


@dataclass
class Campaign:
    """체험단 도메인 엔티티"""
    id: Optional[int]
    advertiser_id: int
    title: str
    description: str
    quota: int
    start_date: date
    end_date: date
    benefits: str
    conditions: str
    image_url: Optional[str]
    status: CampaignStatus
    created_at: datetime
    closed_at: Optional[datetime]

    def is_recruiting(self) -> bool:
        """모집 중인지 확인"""
        return self.status == CampaignStatus.RECRUITING

    def is_selected(self) -> bool:
        """선정 완료 상태인지 확인"""
        return self.status == CampaignStatus.SELECTED

    def is_closed(self) -> bool:
        """모집 종료 상태인지 확인"""
        return self.status == CampaignStatus.CLOSED
