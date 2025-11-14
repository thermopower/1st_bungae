"""User Repository Implementation"""

from typing import Optional
from app.domain.entities.user import User
from app.infrastructure.repositories.interfaces.i_user_repository import IUserRepository
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.mappers.user_mapper import UserMapper
from app.extensions import db


class UserRepository(IUserRepository):
    """User Repository 구현체 (SQLAlchemy)"""

    def find_by_id(self, user_id: str) -> Optional[User]:
        """사용자 ID로 조회"""
        model = db.session.query(UserModel).filter_by(id=user_id).first()
        if model is None:
            return None
        return UserMapper.to_entity(model)

    def find_by_email(self, email: str) -> Optional[User]:
        """이메일로 조회"""
        model = db.session.query(UserModel).filter_by(email=email).first()
        if model is None:
            return None
        return UserMapper.to_entity(model)

    def save(self, user: User) -> User:
        """사용자 저장 (생성 또는 업데이트)"""
        # 기존 사용자 확인
        existing = db.session.query(UserModel).filter_by(id=user.id).first()

        if existing:
            # 업데이트
            existing.email = user.email.value
            existing.role = user.role
        else:
            # 생성
            model = UserMapper.to_model(user)
            db.session.add(model)

        db.session.commit()

        # 저장된 엔티티 반환
        return user

    def exists_by_email(self, email: str) -> bool:
        """이메일 중복 검증"""
        count = db.session.query(UserModel).filter_by(email=email).count()
        return count > 0
