"""Advertiser Repository 구현체"""

from typing import Optional
from app.domain.entities.advertiser import Advertiser
from app.infrastructure.repositories.interfaces.i_advertiser_repository import IAdvertiserRepository
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel
from app.infrastructure.persistence.mappers.advertiser_mapper import AdvertiserMapper
from app.extensions import db


class AdvertiserRepository(IAdvertiserRepository):
    """
    광고주 저장소 구현체

    SQLAlchemy를 사용하여 데이터베이스 접근을 담당합니다.
    """

    def save(self, advertiser: Advertiser) -> Advertiser:
        """
        광고주 정보 저장

        Args:
            advertiser: 광고주 엔티티

        Returns:
            Advertiser: 저장된 광고주 엔티티 (ID 포함)
        """
        model = AdvertiserMapper.to_model(advertiser)
        db.session.add(model)
        db.session.flush()  # ID 생성을 위해 flush

        return AdvertiserMapper.to_entity(model)

    def find_by_user_id(self, user_id: str) -> Optional[Advertiser]:
        """
        사용자 ID로 광고주 조회

        Args:
            user_id: 사용자 ID (UUID)

        Returns:
            Optional[Advertiser]: 광고주 엔티티 (없으면 None)
        """
        model = AdvertiserModel.query.filter_by(user_id=user_id).first()
        return AdvertiserMapper.to_entity(model) if model else None

    def exists_by_business_number(self, business_number: str) -> bool:
        """
        사업자등록번호 중복 검증

        Args:
            business_number: 사업자등록번호 (10자리)

        Returns:
            bool: 존재하면 True, 아니면 False
        """
        count = AdvertiserModel.query.filter_by(business_number=business_number).count()
        return count > 0

    def find_by_id(self, advertiser_id: int) -> Optional[Advertiser]:
        """
        광고주 ID로 조회

        Args:
            advertiser_id: 광고주 ID

        Returns:
            Optional[Advertiser]: 광고주 엔티티 (없으면 None)
        """
        model = AdvertiserModel.query.get(advertiser_id)
        return AdvertiserMapper.to_entity(model) if model else None
