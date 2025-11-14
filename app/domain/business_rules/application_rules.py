"""
Application Business Rules (체험단 지원 비즈니스 규칙)
"""

from typing import Tuple, Optional
from app.domain.entities.campaign import Campaign
from app.domain.entities.influencer import Influencer


class ApplicationRules:
    """체험단 지원 비즈니스 규칙"""

    @staticmethod
    def can_apply(
        campaign: Campaign,
        influencer: Optional[Influencer],
        already_applied: bool
    ) -> Tuple[bool, Optional[str]]:
        """
        지원 가능 여부 검증

        Args:
            campaign: 체험단 엔티티
            influencer: 인플루언서 엔티티 (None 가능)
            already_applied: 이미 지원했는지 여부

        Returns:
            Tuple[bool, Optional[str]]: (가능 여부, 에러 메시지)
        """
        # 인플루언서 정보 등록 여부 검증
        if influencer is None:
            return False, "인플루언서 정보가 등록되지 않았습니다"

        # 체험단 모집 중 상태 검증
        if not campaign.is_recruiting():
            return False, "모집이 종료된 체험단입니다"

        # 중복 지원 검증
        if already_applied:
            return False, "이미 지원한 체험단입니다"

        return True, None
