"""User Mapper (도메인 엔티티 ↔ ORM 모델 변환)"""

from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.infrastructure.persistence.models.user_model import UserModel


class UserMapper:
    """User 도메인 엔티티와 UserModel ORM 간 변환"""

    @staticmethod
    def to_entity(model: UserModel) -> User:
        """
        ORM 모델 → 도메인 엔티티 변환

        Args:
            model: UserModel ORM 객체

        Returns:
            User: 도메인 엔티티
        """
        return User(
            id=model.id,
            email=Email(model.email),
            role=model.role,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        """
        도메인 엔티티 → ORM 모델 변환

        Args:
            entity: User 도메인 엔티티

        Returns:
            UserModel: ORM 모델 객체
        """
        return UserModel(
            id=entity.id,
            email=entity.email.value,
            role=entity.role,
            created_at=entity.created_at
        )
