"""Supabase Auth Provider Implementation"""

from typing import Dict, Any
from app.infrastructure.external.interfaces.i_auth_provider import (
    IAuthProvider,
    AuthUserCreationResult
)
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsException,
    WeakPasswordException,
    InvalidCredentialsException
)
from supabase import create_client, Client
import os


class SupabaseAuthProvider(IAuthProvider):
    """Supabase Auth 구현체"""

    def __init__(self):
        """Supabase 클라이언트 초기화"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

        self.client: Client = create_client(supabase_url, supabase_key)

    def create_user(self, email: str, password: str) -> AuthUserCreationResult:
        """
        Supabase Auth에 사용자 생성

        Args:
            email: 이메일 주소
            password: 비밀번호

        Returns:
            AuthUserCreationResult: 생성된 사용자 정보

        Raises:
            EmailAlreadyExistsException: 이메일 중복
            WeakPasswordException: 비밀번호 강도 미달
        """
        try:
            print(f"[DEBUG] Supabase Auth - 회원가입 요청: {email}")
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })

            print(f"[DEBUG] Supabase Auth - 응답 객체: {response}")

            if response.user is None:
                print(f"[ERROR] Supabase Auth - User가 None임")
                raise Exception("User creation failed")

            print(f"[DEBUG] Supabase Auth - 회원가입 성공: User ID={response.user.id}")
            return AuthUserCreationResult(
                user_id=response.user.id,
                email=response.user.email
            )

        except Exception as e:
            print(f"[ERROR] Supabase Auth - 예외 발생: {type(e).__name__}: {str(e)}")
            error_message = str(e).lower()

            # 이메일 중복 검증
            if "already" in error_message or "exists" in error_message:
                raise EmailAlreadyExistsException(email)

            # 비밀번호 강도 검증
            if "password" in error_message and ("weak" in error_message or "short" in error_message):
                raise WeakPasswordException()

            # 기타 에러
            raise e

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
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.session is None:
                raise InvalidCredentialsException()

            return {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "user_id": response.user.id
            }

        except Exception as e:
            # 인증 실패
            raise InvalidCredentialsException()
