"""Advertiser Application Service"""

from datetime import datetime
from typing import Optional
from app.domain.entities.advertiser import Advertiser
from app.domain.entities.user import User
from app.domain.business_rules.advertiser_rules import AdvertiserRules
from app.domain.exceptions.advertiser_exceptions import (
    AdvertiserAlreadyRegisteredException,
    BusinessNumberAlreadyExistsException
)
from app.infrastructure.repositories.interfaces.i_advertiser_repository import IAdvertiserRepository
from app.infrastructure.repositories.interfaces.i_user_repository import IUserRepository
from app.extensions import db


class AdvertiserService:
    """
    광고주 애플리케이션 서비스

    광고주 정보 등록 및 관리를 담당합니다.
    """

    def __init__(
        self,
        advertiser_repo: IAdvertiserRepository,
        user_repo: IUserRepository
    ):
        """
        AdvertiserService 초기화

        Args:
            advertiser_repo: 광고주 저장소
            user_repo: 사용자 저장소
        """
        self._advertiser_repo = advertiser_repo
        self._user_repo = user_repo

    def register_advertiser(
        self,
        user_id: str,
        name: str,
        birth_date,
        phone_number: str,
        business_name: str,
        address: str,
        business_phone: str,
        business_number: str,
        representative_name: str
    ) -> Advertiser:
        """
        광고주 정보 등록

        Args:
            user_id: 사용자 ID (UUID)
            name: 이름
            birth_date: 생년월일
            phone_number: 휴대폰번호
            business_name: 업체명
            address: 주소
            business_phone: 업장 전화번호
            business_number: 사업자등록번호
            representative_name: 대표자명

        Returns:
            Advertiser: 등록된 광고주 엔티티

        Raises:
            AdvertiserAlreadyRegisteredException: 이미 광고주로 등록된 경우
            BusinessNumberAlreadyExistsException: 사업자등록번호가 중복된 경우
        """
        # 1. 사용자 조회
        user = self._user_repo.find_by_id(user_id)
        if user is None:
            raise ValueError(f"사용자를 찾을 수 없습니다: {user_id}")

        # 2. 광고주 등록 가능 여부 검증 (비즈니스 규칙)
        if not AdvertiserRules.can_register(user):
            raise AdvertiserAlreadyRegisteredException("이미 광고주 또는 인플루언서로 등록되어 있습니다.")

        # 3. 사업자등록번호 중복 검증
        if self._advertiser_repo.exists_by_business_number(business_number):
            raise BusinessNumberAlreadyExistsException(f"사업자등록번호 {business_number}이(가) 이미 존재합니다.")

        # 4. 트랜잭션 시작: User 역할 업데이트 + Advertiser 생성
        try:
            # 4-1. User 역할 업데이트
            user.role = "advertiser"
            self._user_repo.save(user)

            # 4-2. Advertiser 엔티티 생성
            advertiser = Advertiser(
                id=None,
                user_id=user_id,
                name=name,
                birth_date=birth_date,
                phone_number=phone_number,
                business_name=business_name,
                address=address,
                business_phone=business_phone,
                business_number=business_number,
                representative_name=representative_name,
                created_at=datetime.utcnow()
            )

            # 4-3. Advertiser 저장
            saved_advertiser = self._advertiser_repo.save(advertiser)

            # 4-4. 트랜잭션 커밋
            db.session.commit()

            return saved_advertiser

        except Exception as e:
            # 롤백
            db.session.rollback()
            raise e

    def get_advertiser_by_user_id(self, user_id: str) -> Optional[Advertiser]:
        """
        사용자 ID로 광고주 정보 조회

        Args:
            user_id: 사용자 ID (UUID)

        Returns:
            Optional[Advertiser]: 광고주 엔티티 (없으면 None)
        """
        return self._advertiser_repo.find_by_user_id(user_id)
