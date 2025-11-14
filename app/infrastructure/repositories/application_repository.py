# app/infrastructure/repositories/application_repository.py
"""
Application Repository 구현체
체험단 지원 데이터 접근 계층
"""

from sqlalchemy.orm import Session

from app.infrastructure.repositories.interfaces.i_application_repository import IApplicationRepository
from app.infrastructure.persistence.models.application_model import ApplicationModel


class ApplicationRepository(IApplicationRepository):
    """Application Repository 구현"""

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy Session
        """
        self.session = session

    def exists_by_campaign_and_influencer(
        self, campaign_id: int, influencer_id: int
    ) -> bool:
        """
        중복 지원 검증

        Args:
            campaign_id: 체험단 ID
            influencer_id: 인플루언서 ID

        Returns:
            이미 지원했으면 True, 아니면 False
        """
        exists = (
            self.session.query(ApplicationModel)
            .filter_by(campaign_id=campaign_id, influencer_id=influencer_id)
            .first()
        )
        return exists is not None
