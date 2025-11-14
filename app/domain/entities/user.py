"""User Entity (사용자 도메인 엔티티)"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects.email import Email


@dataclass
class User:
    """
    사용자 도메인 엔티티

    Attributes:
        id (str): 사용자 ID (UUID)
        email (Email): 이메일 값 객체
        role (Optional[str]): 사용자 역할 (advertiser/influencer/None)
        created_at (datetime): 계정 생성일
    """

    id: str
    email: Email
    role: Optional[str]
    created_at: datetime

    def has_role(self) -> bool:
        """
        역할이 등록되었는지 확인

        Returns:
            bool: 역할이 등록되어 있으면 True, 아니면 False
        """
        return self.role is not None

    def __eq__(self, other) -> bool:
        """동등성: ID가 같으면 동일한 사용자"""
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """해시: ID 기반"""
        return hash(self.id)
