"""
Influencer Mapper (Entity ↔ Model 변환)
"""
from app.domain.entities.influencer import Influencer
from app.infrastructure.persistence.models.influencer_model import InfluencerModel


class InfluencerMapper:
    """인플루언서 엔티티와 ORM 모델 간 변환"""

    @staticmethod
    def to_entity(model: InfluencerModel) -> Influencer:
        """
        ORM 모델 → 도메인 엔티티

        Args:
            model: InfluencerModel 인스턴스

        Returns:
            Influencer: 도메인 엔티티
        """
        return Influencer(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            birth_date=model.birth_date,
            phone_number=model.phone_number,
            channel_name=model.channel_name,
            channel_url=model.channel_url,
            follower_count=model.follower_count,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: Influencer) -> InfluencerModel:
        """
        도메인 엔티티 → ORM 모델

        Args:
            entity: Influencer 엔티티

        Returns:
            InfluencerModel: ORM 모델
        """
        model = InfluencerModel()
        if entity.id is not None:
            model.id = entity.id
        model.user_id = entity.user_id
        model.name = entity.name
        model.birth_date = entity.birth_date
        model.phone_number = entity.phone_number
        model.channel_name = entity.channel_name
        model.channel_url = entity.channel_url
        model.follower_count = entity.follower_count
        model.created_at = entity.created_at
        return model
