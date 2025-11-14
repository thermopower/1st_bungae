# app/infrastructure/persistence/mappers/application_mapper.py
"""
Application Mapper
Application 엔티티 ↔ ApplicationModel ORM 변환
"""

from app.domain.entities.application import Application
from app.infrastructure.persistence.models.application_model import ApplicationModel


class ApplicationMapper:
    """Application 도메인 엔티티와 ORM 모델 간 매핑"""

    @staticmethod
    def to_entity(model: ApplicationModel) -> Application:
        """
        ORM 모델 → 도메인 엔티티

        Args:
            model: ApplicationModel ORM 객체

        Returns:
            Application 도메인 엔티티
        """
        return Application(
            id=model.id,
            campaign_id=model.campaign_id,
            influencer_id=model.influencer_id,
            application_reason=model.application_reason,
            status=model.status,
            applied_at=model.applied_at
        )

    @staticmethod
    def to_model(entity: Application) -> ApplicationModel:
        """
        도메인 엔티티 → ORM 모델

        Args:
            entity: Application 도메인 엔티티

        Returns:
            ApplicationModel ORM 객체
        """
        model = ApplicationModel(
            campaign_id=entity.campaign_id,
            influencer_id=entity.influencer_id,
            application_reason=entity.application_reason,
            status=entity.status,
            applied_at=entity.applied_at
        )

        if entity.id is not None:
            model.id = entity.id

        return model
