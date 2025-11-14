# app/application/services/campaign_service.py
"""
Campaign Service
체험단 비즈니스 로직
"""

from typing import List, Optional, Tuple
from datetime import date

from app.domain.entities.campaign import Campaign
from app.infrastructure.repositories.interfaces.i_campaign_repository import ICampaignRepository
from app.infrastructure.repositories.interfaces.i_influencer_repository import IInfluencerRepository
from app.infrastructure.repositories.interfaces.i_application_repository import IApplicationRepository
from app.presentation.schemas.campaign_schemas import CampaignDetailDTO, CampaignListItemDTO


class CampaignService:
    """Campaign Service 구현"""

    def __init__(
        self,
        campaign_repository: ICampaignRepository,
        influencer_repository: IInfluencerRepository = None,
        application_repository: IApplicationRepository = None
    ):
        """
        Args:
            campaign_repository: CampaignRepository
            influencer_repository: InfluencerRepository (optional)
            application_repository: ApplicationRepository (optional)
        """
        self.campaign_repository = campaign_repository
        self.influencer_repository = influencer_repository
        self.application_repository = application_repository

    def get_campaign_detail(
        self, campaign_id: int, user_id: Optional[str] = None
    ) -> Optional[CampaignDetailDTO]:
        """
        체험단 상세 정보 조회

        Args:
            campaign_id: 체험단 ID
            user_id: 사용자 ID (로그인 시)

        Returns:
            CampaignDetailDTO 또는 None
        """
        # 체험단 조회 (광고주 정보 포함)
        result = self.campaign_repository.find_by_id_with_advertiser(campaign_id)
        if result is None:
            return None

        campaign, business_name, business_address = result

        # 지원자 수 조회
        application_count = self.campaign_repository.get_application_count(campaign_id)

        # 지원 가능 여부 확인
        can_apply = False
        already_applied = False

        if user_id and self.influencer_repository and self.application_repository:
            # 인플루언서 정보 확인
            influencer = self.influencer_repository.find_by_user_id(user_id)
            if influencer and campaign.is_recruiting():
                can_apply = True
                # 중복 지원 확인
                already_applied = self.application_repository.exists_by_campaign_and_influencer(
                    campaign_id, influencer.id
                )
                if already_applied:
                    can_apply = False

        return CampaignDetailDTO(
            id=campaign.id,
            title=campaign.title,
            description=campaign.description,
            image_url=campaign.image_url,
            quota=campaign.quota,
            application_count=application_count,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            benefits=campaign.benefits,
            conditions=campaign.conditions,
            status=campaign.status.value,
            business_name=business_name,
            business_address=business_address,
            can_apply=can_apply,
            already_applied=already_applied
        )

    def list_recruiting_campaigns(
        self, page: int = 1, per_page: int = 12, sort: str = 'latest'
    ) -> Tuple[List[CampaignListItemDTO], int]:
        """
        모집 중인 체험단 목록 조회

        Args:
            page: 페이지 번호 (1부터 시작)
            per_page: 페이지당 레코드 수
            sort: 정렬 기준 ('latest', 'deadline', 'popular')

        Returns:
            (campaigns, total_count) 튜플
        """
        skip = (page - 1) * per_page

        # 체험단 목록 조회
        results = self.campaign_repository.find_recruiting_campaigns(
            skip=skip, limit=per_page, sort=sort
        )

        # DTO 변환
        campaign_dtos = [
            CampaignListItemDTO(
                id=campaign.id,
                title=campaign.title,
                description_short=campaign.description[:100],
                image_url=campaign.image_url,
                quota=campaign.quota,
                application_count=application_count,
                deadline=campaign.end_date,
                business_name=business_name,
                status=campaign.status.value
            )
            for campaign, business_name, application_count in results
        ]

        # 총 개수 조회
        total_count = self.campaign_repository.count_recruiting_campaigns()

        return (campaign_dtos, total_count)
