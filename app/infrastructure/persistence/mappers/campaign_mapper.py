# app/infrastructure/persistence/mappers/campaign_mapper.py
"""
Campaign Mapper (도메인 엔티티 ↔ ORM 모델 변환)
"""

from app.domain.entities.campaign import Campaign, CampaignStatus
from app.infrastructure.persistence.models.campaign_model import CampaignModel


class CampaignMapper:
    """Campaign 도메인 엔티티와 CampaignModel ORM 간 변환"""

    @staticmethod
    def to_entity(model: CampaignModel) -> Campaign:
        """
        ORM 모델 → 도메인 엔티티 변환

        Args:
            model: CampaignModel ORM 객체

        Returns:
            Campaign: 도메인 엔티티
        """
        return Campaign(
            id=model.id,
            advertiser_id=model.advertiser_id,
            title=model.title,
            description=model.description,
            quota=model.quota,
            start_date=model.start_date,
            end_date=model.end_date,
            benefits=model.benefits,
            conditions=model.conditions,
            image_url=model.image_url,
            status=CampaignStatus(model.status),
            created_at=model.created_at,
            closed_at=model.closed_at
        )

    @staticmethod
    def to_model(entity: Campaign) -> CampaignModel:
        """
        도메인 엔티티 → ORM 모델 변환

        Args:
            entity: Campaign 도메인 엔티티

        Returns:
            CampaignModel: ORM 모델 객체
        """
        model = CampaignModel(
            advertiser_id=entity.advertiser_id,
            title=entity.title,
            description=entity.description,
            quota=entity.quota,
            start_date=entity.start_date,
            end_date=entity.end_date,
            benefits=entity.benefits,
            conditions=entity.conditions,
            image_url=entity.image_url,
            status=entity.status.value,
            created_at=entity.created_at,
            closed_at=entity.closed_at
        )

        # ID가 있으면 설정 (업데이트 케이스)
        if entity.id is not None:
            model.id = entity.id

        return model
