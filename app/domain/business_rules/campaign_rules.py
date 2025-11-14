# app/domain/business_rules/campaign_rules.py
"""
Campaign 비즈니스 규칙
체험단 관련 도메인 로직
"""

from datetime import date
from app.domain.entities.campaign import Campaign, CampaignStatus


class CampaignRules:
    """Campaign 비즈니스 규칙"""

    @staticmethod
    def can_close_early(campaign: Campaign) -> bool:
        """
        조기종료 가능 여부 검증

        Args:
            campaign: Campaign 엔티티

        Returns:
            bool: 조기종료 가능 여부
        """
        return campaign.status == CampaignStatus.RECRUITING

    @staticmethod
    def can_select_influencers(campaign: Campaign) -> bool:
        """
        인플루언서 선정 가능 여부 검증

        Args:
            campaign: Campaign 엔티티

        Returns:
            bool: 선정 가능 여부
        """
        return campaign.status == CampaignStatus.CLOSED

    @staticmethod
    def validate_selection_count(campaign: Campaign, selected_count: int) -> bool:
        """
        선정 인원 검증

        Args:
            campaign: Campaign 엔티티
            selected_count: 선정할 인플루언서 수

        Returns:
            bool: 선정 인원이 모집 인원 이하인지 여부
        """
        return selected_count <= campaign.quota

    @staticmethod
    def validate_campaign_dates(start_date: date, end_date: date) -> bool:
        """
        모집 기간 검증

        Args:
            start_date: 모집 시작일
            end_date: 모집 종료일

        Returns:
            bool: 모집 기간이 유효한지 여부
        """
        today = date.today()

        # 시작일이 과거인지 검증
        if start_date < today:
            return False

        # 종료일이 시작일보다 앞서는지 검증
        if end_date <= start_date:
            return False

        return True
