"""Auth Service (회원가입, 로그인 유스케이스)"""

from datetime import datetime, UTC
from typing import Dict, Any
from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.business_rules.user_rules import UserRules
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsException,
    WeakPasswordException,
    InvalidCredentialsException
)
from app.infrastructure.repositories.interfaces.i_user_repository import IUserRepository
from app.infrastructure.external.interfaces.i_auth_provider import (
    IAuthProvider,
    AuthUserCreationResult
)


class RegisterResponse:
    """회원가입 응답 DTO"""

    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email


class LoginResponse:
    """로그인 응답 DTO"""

    def __init__(
        self,
        user_id: str,
        email: str,
        role: str | None,
        access_token: str,
        refresh_token: str,
        redirect_url: str
    ):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.redirect_url = redirect_url


class AuthService:
    """인증 서비스 (Application Layer)"""

    def __init__(
        self,
        user_repository: IUserRepository,
        auth_provider: IAuthProvider
    ):
        """
        AuthService 초기화

        Args:
            user_repository: User Repository
            auth_provider: Auth Provider (Supabase Auth)
        """
        self.user_repository = user_repository
        self.auth_provider = auth_provider

    def register(self, email: str, password: str) -> RegisterResponse:
        """
        회원가입 처리

        Args:
            email: 이메일 주소
            password: 비밀번호

        Returns:
            RegisterResponse: 회원가입 응답 (user_id, email)

        Raises:
            InvalidEmailException: 이메일 형식 오류
            EmailAlreadyExistsException: 이메일 중복
            WeakPasswordException: 비밀번호 강도 미달
        """
        # 1. 이메일 검증 (Value Object)
        email_vo = Email(email)

        # 2. 비밀번호 강도 검증 (Business Rules)
        if not UserRules.validate_password_strength(password):
            raise WeakPasswordException()

        # 3. 이메일 중복 검증
        if self.user_repository.exists_by_email(email):
            raise EmailAlreadyExistsException(email)

        # 4. Supabase Auth에 사용자 생성
        auth_result: AuthUserCreationResult = self.auth_provider.create_user(email, password)

        # 5. User 테이블에 레코드 생성
        user = User(
            id=auth_result.user_id,
            email=email_vo,
            role=None,  # 역할은 나중에 등록
            created_at=datetime.now(UTC)
        )

        self.user_repository.save(user)

        # 6. 응답 반환
        return RegisterResponse(
            user_id=auth_result.user_id,
            email=auth_result.email
        )

    def login(self, email: str, password: str) -> LoginResponse:
        """
        로그인 처리

        Args:
            email: 이메일 주소
            password: 비밀번호

        Returns:
            LoginResponse: 로그인 응답

        Raises:
            InvalidCredentialsException: 이메일 또는 비밀번호 불일치
        """
        # 1. Supabase Auth 인증
        auth_result: Dict[str, Any] = self.auth_provider.authenticate(email, password)

        # 2. User 정보 조회
        user = self.user_repository.find_by_id(auth_result['user_id'])

        if user is None:
            # User 테이블에 없으면 생성 (회원가입 직후 바로 로그인한 경우)
            user = User(
                id=auth_result['user_id'],
                email=Email(email),
                role=None,
                created_at=datetime.now(UTC)
            )
            self.user_repository.save(user)

        # 3. 역할에 따른 리다이렉트 URL 결정
        redirect_url = UserRules.determine_redirect_url(user)

        # 4. 응답 반환
        return LoginResponse(
            user_id=user.id,
            email=user.email.value,
            role=user.role,
            access_token=auth_result['access_token'],
            refresh_token=auth_result['refresh_token'],
            redirect_url=redirect_url
        )
