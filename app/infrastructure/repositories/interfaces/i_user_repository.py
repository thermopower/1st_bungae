"""User Repository Interface"""

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class IUserRepository(ABC):
    """User Repository 인터페이스"""

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        사용자 ID로 조회

        Args:
            user_id: 사용자 ID (UUID)

        Returns:
            User | None: 사용자 엔티티 또는 None
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 조회

        Args:
            email: 이메일 주소

        Returns:
            User | None: 사용자 엔티티 또는 None
        """
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """
        사용자 저장 (생성 또는 업데이트)

        Args:
            user: User 도메인 엔티티

        Returns:
            User: 저장된 사용자 엔티티
        """
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        이메일 중복 검증

        Args:
            email: 이메일 주소

        Returns:
            bool: 존재하면 True, 아니면 False
        """
        pass
