"""
Influencer Application Service
"""
from datetime import datetime
from typing import Optional
from app.domain.entities.influencer import Influencer
from app.domain.entities.user import User
from app.domain.business_rules.influencer_rules import InfluencerRules
from app.domain.exceptions.influencer_exceptions import (
    InfluencerAlreadyRegisteredException,
    InfluencerNotFoundException
)
from app.infrastructure.repositories.interfaces.i_influencer_repository import IInfluencerRepository
from app.infrastructure.repositories.interfaces.i_user_repository import IUserRepository
from app.extensions import db


class InfluencerService:
    """
    인플루언서 애플리케이션 서비스

    인플루언서 정보 등록 및 관리를 담당합니다.
    """

    def __init__(
        self,
        influencer_repo: IInfluencerRepository,
        user_repo: IUserRepository
    ):
        """
        InfluencerService 초기화

        Args:
            influencer_repo: 인플루언서 저장소
            user_repo: 사용자 저장소
        """
        self._influencer_repo = influencer_repo
        self._user_repo = user_repo

    def register_influencer(
        self,
        user_id: str,
        name: str,
        birth_date,
        phone_number: str,
        channel_name: str,
        channel_url: str,
        follower_count: int
    ) -> Influencer:
        """
        인플루언서 정보 등록

        Args:
            user_id: 사용자 ID (UUID)
            name: 이름
            birth_date: 생년월일
            phone_number: 휴대폰번호
            channel_name: SNS 채널명
            channel_url: 채널 링크
            follower_count: 팔로워 수

        Returns:
            Influencer: 등록된 인플루언서 엔티티

        Raises:
            InfluencerAlreadyRegisteredException: 이미 인플루언서로 등록된 경우
            ValueError: 사용자를 찾을 수 없거나 팔로워 수가 유효하지 않은 경우
        """
        # 1. 사용자 조회
        user = self._user_repo.find_by_id(user_id)
        if user is None:
            raise ValueError(f"사용자를 찾을 수 없습니다: {user_id}")

        # 2. 인플루언서 등록 가능 여부 검증 (비즈니스 규칙)
        # 이미 인플루언서 정보를 등록했는지 확인
        existing_influencer = self._influencer_repo.find_by_user_id(user_id)
        if existing_influencer is not None:
            raise InfluencerAlreadyRegisteredException("이미 인플루언서 정보가 등록되어 있습니다.")

        # 3. 팔로워 수 검증 (비즈니스 규칙)
        if not InfluencerRules.validate_follower_count(follower_count):
            raise ValueError(f"팔로워 수는 0 이상이어야 합니다: {follower_count}")

        # 4. 트랜잭션 시작: User 역할 업데이트 + Influencer 생성
        try:
            # 4-1. User 역할 업데이트
            user.role = "influencer"
            self._user_repo.save(user)

            # 4-2. Influencer 엔티티 생성
            influencer = Influencer(
                id=None,
                user_id=user_id,
                name=name,
                birth_date=birth_date,
                phone_number=phone_number,
                channel_name=channel_name,
                channel_url=channel_url,
                follower_count=follower_count,
                created_at=datetime.now()
            )

            # 4-3. Influencer 저장
            saved_influencer = self._influencer_repo.save(influencer)

            # 5. 트랜잭션 커밋
            db.session.commit()

            return saved_influencer

        except Exception as e:
            # 롤백
            db.session.rollback()
            raise e

    def get_influencer_by_user_id(self, user_id: str) -> Optional[Influencer]:
        """
        사용자 ID로 인플루언서 정보 조회

        Args:
            user_id: 사용자 ID

        Returns:
            Optional[Influencer]: 인플루언서 엔티티 또는 None
        """
        return self._influencer_repo.find_by_user_id(user_id)
