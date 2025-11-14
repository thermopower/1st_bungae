# app/infrastructure/repositories/application_repository.py
"""
Application Repository 구현체
체험단 지원 데이터 접근 계층
"""

from typing import List
from sqlalchemy.orm import Session

from app.domain.entities.application import Application
from app.infrastructure.repositories.interfaces.i_application_repository import IApplicationRepository
from app.infrastructure.persistence.models.application_model import ApplicationModel
from app.infrastructure.persistence.mappers.application_mapper import ApplicationMapper


class ApplicationRepository(IApplicationRepository):
    """Application Repository 구현"""

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy Session
        """
        self.session = session

    def save(self, application: Application) -> Application:
        """
        지원 정보 저장

        Args:
            application: Application 엔티티

        Returns:
            저장된 Application 엔티티 (ID 포함)
        """
        model = ApplicationMapper.to_model(application)
        self.session.add(model)
        self.session.flush()
        return ApplicationMapper.to_entity(model)

    def find_by_campaign_id(self, campaign_id: int) -> List[Application]:
        """
        체험단의 지원자 목록 조회

        Args:
            campaign_id: 체험단 ID

        Returns:
            Application 엔티티 리스트
        """
        models = (
            self.session.query(ApplicationModel)
            .filter_by(campaign_id=campaign_id)
            .order_by(ApplicationModel.applied_at.desc())
            .all()
        )
        return [ApplicationMapper.to_entity(model) for model in models]

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

    def update_status_bulk(
        self, application_ids: List[int], status: str
    ) -> None:
        """
        지원 상태 일괄 업데이트

        Args:
            application_ids: 업데이트할 지원 ID 리스트
            status: 변경할 상태
        """
        self.session.query(ApplicationModel).filter(
            ApplicationModel.id.in_(application_ids)
        ).update(
            {"status": status},
            synchronize_session=False
        )
