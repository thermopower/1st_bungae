"""
Influencer Repository 구현체
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.influencer import Influencer
from app.infrastructure.repositories.interfaces.i_influencer_repository import IInfluencerRepository
from app.infrastructure.persistence.models.influencer_model import InfluencerModel
from app.infrastructure.persistence.mappers.influencer_mapper import InfluencerMapper


class InfluencerRepository(IInfluencerRepository):
    """인플루언서 리포지토리 구현체"""

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy Session
        """
        self.session = session

    def save(self, influencer: Influencer) -> Influencer:
        """인플루언서 정보 저장"""
        model = InfluencerMapper.to_model(influencer)
        self.session.add(model)
        self.session.flush()  # ID 생성을 위한 flush
        return InfluencerMapper.to_entity(model)

    def find_by_user_id(self, user_id: str) -> Optional[Influencer]:
        """사용자 ID로 인플루언서 조회"""
        model = self.session.query(InfluencerModel).filter_by(user_id=user_id).first()
        return InfluencerMapper.to_entity(model) if model else None

    def find_by_id(self, influencer_id: int) -> Optional[Influencer]:
        """인플루언서 ID로 조회"""
        model = self.session.get(InfluencerModel, influencer_id)
        return InfluencerMapper.to_entity(model) if model else None

    def exists_by_user_id(self, user_id: str) -> bool:
        """사용자 ID로 인플루언서 존재 여부 확인"""
        count = self.session.query(InfluencerModel).filter_by(user_id=user_id).count()
        return count > 0
