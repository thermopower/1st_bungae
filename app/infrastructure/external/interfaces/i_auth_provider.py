"""Auth Provider Interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AuthUserCreationResult:
    """사용자 생성 결과"""
    user_id: str
    email: str


class IAuthProvider(ABC):
    """인증 제공자 인터페이스 (Supabase Auth)"""

    @abstractmethod
    def create_user(self, email: str, password: str) -> AuthUserCreationResult:
        """
        사용자 생성 (Supabase Auth)

        Args:
            email: 이메일 주소
            password: 비밀번호

        Returns:
            AuthUserCreationResult: 생성된 사용자 정보 (user_id, email)

        Raises:
            EmailAlreadyExistsException: 이메일 중복
            WeakPasswordException: 비밀번호 강도 미달
        """
        pass

    @abstractmethod
    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """
        사용자 인증 (로그인)

        Args:
            email: 이메일 주소
            password: 비밀번호

        Returns:
            Dict: 세션 정보 (access_token, refresh_token)

        Raises:
            InvalidCredentialsException: 이메일 또는 비밀번호 불일치
        """
        pass
