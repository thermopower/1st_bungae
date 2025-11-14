"""
Application Entity (체험단 지원 도메인 엔티티)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.shared.constants.campaign_constants import (
    APPLICATION_STATUS_APPLIED,
    APPLICATION_STATUS_SELECTED,
    APPLICATION_STATUS_REJECTED,
)


@dataclass
class Application:
    """체험단 지원 도메인 엔티티"""

    id: Optional[int]
    campaign_id: int
    influencer_id: int
    application_reason: Optional[str]
    status: str
    applied_at: datetime

    def is_applied(self) -> bool:
        """지원 완료 상태인지 확인"""
        return self.status == APPLICATION_STATUS_APPLIED

    def is_selected(self) -> bool:
        """선정된 상태인지 확인"""
        return self.status == APPLICATION_STATUS_SELECTED

    def is_rejected(self) -> bool:
        """탈락 상태인지 확인"""
        return self.status == APPLICATION_STATUS_REJECTED
