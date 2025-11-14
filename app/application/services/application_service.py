# app/application/services/application_service.py
"""
Application Service
체험단 지원 비즈니스 로직
"""

from typing import List
from app.domain.entities.application import Application
from app.domain.entities.campaign import Campaign, CampaignStatus
from app.infrastructure.repositories.interfaces.i_application_repository import IApplicationRepository
from app.infrastructure.repositories.interfaces.i_campaign_repository import ICampaignRepository
from app.domain.exceptions.campaign_exceptions import (
    CampaignNotFoundException,
    CampaignNotOwnedException,
    InvalidCampaignStatusException,
    SelectionQuotaExceededException,
)
from app.shared.constants.campaign_constants import (
    APPLICATION_STATUS_SELECTED,
    APPLICATION_STATUS_REJECTED,
)


class ApplicationService:
    """Application Service 구현"""

    def __init__(
        self,
        application_repository: IApplicationRepository,
        campaign_repository: ICampaignRepository,
    ):
        """
        Args:
            application_repository: ApplicationRepository
            campaign_repository: CampaignRepository
        """
        self.application_repository = application_repository
        self.campaign_repository = campaign_repository

    def select_influencers(
        self,
        campaign_id: int,
        advertiser_id: int,
        selected_application_ids: List[int],
    ) -> None:
        """
        인플루언서 선정

        Args:
            campaign_id: 체험단 ID
            advertiser_id: 광고주 ID (권한 검증용)
            selected_application_ids: 선정할 지원 ID 리스트

        Raises:
            CampaignNotFoundException: 체험단이 존재하지 않음
            CampaignNotOwnedException: 체험단 소유권이 없음
            InvalidCampaignStatusException: 체험단 상태가 CLOSED가 아님
            SelectionQuotaExceededException: 선정 인원 초과
        """
        # 체험단 조회
        campaign = self.campaign_repository.find_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundException("체험단을 찾을 수 없습니다")

        # 소유권 검증
        if campaign.advertiser_id != advertiser_id:
            raise CampaignNotOwnedException("이 체험단에 대한 권한이 없습니다")

        # 모집 종료 상태 검증
        if not campaign.is_closed():
            raise InvalidCampaignStatusException("모집이 종료된 체험단만 선정할 수 있습니다")

        # 선정 인원 검증
        if len(selected_application_ids) > campaign.quota:
            raise SelectionQuotaExceededException(
                f"선정 인원은 모집 인원({campaign.quota}명)을 초과할 수 없습니다"
            )

        # 선정된 인플루언서 상태 업데이트
        self.application_repository.update_status_bulk(
            selected_application_ids, APPLICATION_STATUS_SELECTED
        )

        # 미선정 인플루언서 상태 업데이트
        all_applications = self.application_repository.find_by_campaign_id(campaign_id)
        rejected_ids = [
            app.id for app in all_applications
            if app.id not in selected_application_ids and app.is_applied()
        ]
        if rejected_ids:
            self.application_repository.update_status_bulk(
                rejected_ids, APPLICATION_STATUS_REJECTED
            )

        # 체험단 상태 업데이트
        campaign.status = CampaignStatus.SELECTED
        self.campaign_repository.save(campaign)
