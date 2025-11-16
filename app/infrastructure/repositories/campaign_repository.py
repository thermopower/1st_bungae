# app/infrastructure/repositories/campaign_repository.py
"""
Campaign Repository 구현체
체험단 데이터 접근 계층
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.domain.entities.campaign import Campaign
from app.infrastructure.repositories.interfaces.i_campaign_repository import ICampaignRepository
from app.infrastructure.persistence.models.campaign_model import CampaignModel
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel
from app.infrastructure.persistence.models.application_model import ApplicationModel
from app.infrastructure.persistence.mappers.campaign_mapper import CampaignMapper


class CampaignRepository(ICampaignRepository):
    """Campaign Repository 구현"""

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy Session
        """
        self.session = session

    def find_by_id(self, campaign_id: int) -> Optional[Campaign]:
        """
        체험단 ID로 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            Campaign 엔티티 또는 None
        """
        model = self.session.query(CampaignModel).filter_by(id=campaign_id).first()
        if model is None:
            return None
        return CampaignMapper.to_entity(model)

    def find_by_id_with_advertiser(self, campaign_id: int) -> Optional[tuple]:
        """
        체험단 ID로 광고주 정보 포함하여 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            (Campaign, business_name, business_address) 튜플 또는 None
        """
        result = (
            self.session.query(
                CampaignModel,
                AdvertiserModel.business_name,
                AdvertiserModel.address
            )
            .join(AdvertiserModel, CampaignModel.advertiser_id == AdvertiserModel.id)
            .filter(CampaignModel.id == campaign_id)
            .first()
        )

        if result is None:
            return None

        campaign_model, business_name, business_address = result
        campaign = CampaignMapper.to_entity(campaign_model)
        return (campaign, business_name, business_address)

    def get_application_count(self, campaign_id: int) -> int:
        """
        지원자 수 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            지원자 수
        """
        count = (
            self.session.query(func.count(ApplicationModel.id))
            .filter(ApplicationModel.campaign_id == campaign_id)
            .scalar()
        )
        return count or 0

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
        # 서브쿼리: 지원자 수 집계
        application_count_subq = (
            self.session.query(
                ApplicationModel.campaign_id,
                func.count(ApplicationModel.id).label('application_count')
            )
            .group_by(ApplicationModel.campaign_id)
            .subquery()
        )

        # 메인 쿼리
        query = (
            self.session.query(
                CampaignModel,
                AdvertiserModel.business_name,
                func.coalesce(application_count_subq.c.application_count, 0).label('application_count')
            )
            .join(AdvertiserModel, CampaignModel.advertiser_id == AdvertiserModel.id)
            .outerjoin(application_count_subq, CampaignModel.id == application_count_subq.c.campaign_id)
            .filter(CampaignModel.status == 'RECRUITING')
        )

        # 정렬
        if sort == 'latest':
            query = query.order_by(desc(CampaignModel.created_at))
        elif sort == 'deadline':
            query = query.order_by(CampaignModel.end_date)
        elif sort == 'popular':
            query = query.order_by(desc('application_count'))
        else:
            query = query.order_by(desc(CampaignModel.created_at))

        # 페이지네이션
        query = query.offset(skip).limit(limit)

        # 결과 변환
        results = query.all()
        return [
            (
                CampaignMapper.to_entity(campaign_model),
                business_name,
                application_count
            )
            for campaign_model, business_name, application_count in results
        ]

    def count_recruiting_campaigns(self) -> int:
        """
        모집 중인 체험단 총 개수 조회

        Returns:
            총 개수
        """
        count = (
            self.session.query(func.count(CampaignModel.id))
            .filter(CampaignModel.status == 'RECRUITING')
            .scalar()
        )
        return count or 0

    def find_by_advertiser_id(self, advertiser_id: int) -> List[Campaign]:
        """
        광고주 ID로 체험단 목록 조회

        Args:
            advertiser_id: 광고주 ID

        Returns:
            Campaign 엔티티 리스트
        """
        models = (
            self.session.query(CampaignModel)
            .filter(CampaignModel.advertiser_id == advertiser_id)
            .order_by(desc(CampaignModel.created_at))
            .all()
        )
        return [CampaignMapper.to_entity(model) for model in models]

    def save(self, campaign: Campaign) -> Campaign:
        """
        체험단 저장

        Args:
            campaign: Campaign 엔티티

        Returns:
            저장된 Campaign 엔티티 (ID 포함)
        """
        model = CampaignMapper.to_model(campaign)
        self.session.add(model)
        self.session.flush()  # ID 생성
        return CampaignMapper.to_entity(model)
