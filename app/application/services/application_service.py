# app/application/services/application_service.py
"""
Application Service
체험단 지원 비즈니스 로직
"""

from typing import List
from datetime import datetime
from app.domain.entities.application import Application
from app.domain.entities.campaign import Campaign, CampaignStatus
from app.infrastructure.repositories.interfaces.i_application_repository import IApplicationRepository
from app.infrastructure.repositories.interfaces.i_campaign_repository import ICampaignRepository
from app.infrastructure.repositories.interfaces.i_influencer_repository import IInfluencerRepository
from app.domain.exceptions.campaign_exceptions import (
    CampaignNotFoundException,
    CampaignNotOwnedException,
    InvalidCampaignStatusException,
    SelectionQuotaExceededException,
)
from app.domain.exceptions.application_exceptions import (
    AlreadyAppliedException,
    CampaignNotRecruitingException,
    InfluencerNotRegisteredException,
)
from app.domain.business_rules.application_rules import ApplicationRules
from app.shared.constants.campaign_constants import (
    APPLICATION_STATUS_APPLIED,
    APPLICATION_STATUS_SELECTED,
    APPLICATION_STATUS_REJECTED,
)


class ApplicationService:
    """Application Service 구현"""

    def __init__(
        self,
        application_repository: IApplicationRepository,
        campaign_repository: ICampaignRepository,
        influencer_repository: IInfluencerRepository,
    ):
        """
        Args:
            application_repository: ApplicationRepository
            campaign_repository: CampaignRepository
            influencer_repository: InfluencerRepository
        """
        self.application_repository = application_repository
        self.campaign_repository = campaign_repository
        self.influencer_repository = influencer_repository

    def apply_to_campaign(
        self,
        campaign_id: int,
        influencer_id: int,
        application_reason: str = None,
    ) -> Application:
        """
        체험단 지원 처리

        Args:
            campaign_id: 체험단 ID
            influencer_id: 인플루언서 ID
            application_reason: 지원 사유 (선택)

        Returns:
            Application: 생성된 지원 엔티티

        Raises:
            CampaignNotFoundException: 체험단이 존재하지 않음
            InfluencerNotRegisteredException: 인플루언서 정보가 등록되지 않음
            CampaignNotRecruitingException: 모집이 종료된 체험단
            AlreadyAppliedException: 이미 지원한 체험단
        """
        # 1. 체험단 조회
        campaign = self.campaign_repository.find_by_id(campaign_id)
        if campaign is None:
            raise CampaignNotFoundException("체험단을 찾을 수 없습니다")

        # 2. 인플루언서 조회
        influencer = self.influencer_repository.find_by_id(influencer_id)

        # 3. 중복 지원 확인
        already_applied = self.application_repository.exists_by_campaign_and_influencer(
            campaign_id, influencer_id
        )

        # 4. 지원 가능 여부 검증 (비즈니스 규칙)
        can_apply, error_message = ApplicationRules.can_apply(
            campaign, influencer, already_applied
        )

        if not can_apply:
            # 에러 메시지에 따라 적절한 예외 발생
            if "인플루언서" in error_message:
                raise InfluencerNotRegisteredException(error_message)
            elif "모집이 종료" in error_message:
                raise CampaignNotRecruitingException(error_message)
            elif "이미 지원" in error_message:
                raise AlreadyAppliedException(error_message)
            else:
                raise Exception(error_message)

        # 5. Application 엔티티 생성
        application = Application(
            id=None,
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            application_reason=application_reason,
            status=APPLICATION_STATUS_APPLIED,
            applied_at=datetime.now()
        )

        # 6. 저장
        saved_application = self.application_repository.save(application)

        return saved_application

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
