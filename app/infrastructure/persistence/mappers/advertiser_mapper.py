"""Advertiser Mapper (도메인 엔티티 ↔ ORM 모델 변환)"""

from app.domain.entities.advertiser import Advertiser
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel


class AdvertiserMapper:
    """
    Advertiser Entity와 AdvertiserModel 간 변환을 담당하는 매퍼

    Domain Layer와 Infrastructure Layer 간의 경계를 유지합니다.
    """

    @staticmethod
    def to_entity(model: AdvertiserModel) -> Advertiser:
        """
        ORM 모델 → 도메인 엔티티 변환

        Args:
            model: AdvertiserModel (SQLAlchemy ORM)

        Returns:
            Advertiser: 도메인 엔티티
        """
        if model is None:
            return None

        return Advertiser(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            birth_date=model.birth_date,
            phone_number=model.phone_number,
            business_name=model.business_name,
            address=model.address,
            business_phone=model.business_phone,
            business_number=model.business_number,
            representative_name=model.representative_name,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: Advertiser) -> AdvertiserModel:
        """
        도메인 엔티티 → ORM 모델 변환

        Args:
            entity: Advertiser 도메인 엔티티

        Returns:
            AdvertiserModel: SQLAlchemy ORM 모델
        """
        model = AdvertiserModel()

        if entity.id is not None:
            model.id = entity.id

        model.user_id = entity.user_id
        model.name = entity.name
        model.birth_date = entity.birth_date
        model.phone_number = entity.phone_number
        model.business_name = entity.business_name
        model.address = entity.address
        model.business_phone = entity.business_phone
        model.business_number = entity.business_number
        model.representative_name = entity.representative_name
        model.created_at = entity.created_at

        return model
