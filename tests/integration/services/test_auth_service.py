"""Auth Service Integration Tests"""

import pytest
from unittest.mock import Mock, MagicMock
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.external.supabase.supabase_auth import SupabaseAuthProvider
from app.infrastructure.external.interfaces.i_auth_provider import AuthUserCreationResult
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsException,
    WeakPasswordException
)


class TestAuthServiceIntegration:
    """AuthService 통합 테스트"""

    def setup_method(self):
        """각 테스트 전 실행"""
        # Mock Repository
        self.user_repository = Mock(spec=UserRepository)

        # Mock Auth Provider
        self.auth_provider = Mock(spec=SupabaseAuthProvider)

        # AuthService 인스턴스
        self.auth_service = AuthService(
            user_repository=self.user_repository,
            auth_provider=self.auth_provider
        )

    def test_register_success(self):
        """정상 케이스: 회원가입 성공"""
        # Given: 유효한 이메일과 비밀번호
        email = "test@example.com"
        password = "Password123"

        # Mock 설정
        self.user_repository.exists_by_email.return_value = False
        self.auth_provider.create_user.return_value = AuthUserCreationResult(
            user_id="test-uuid-1234",
            email=email
        )

        # When: 회원가입 호출
        response = self.auth_service.register(email, password)

        # Then: 성공 응답
        assert response.user_id == "test-uuid-1234"
        assert response.email == email

        # Repository 메서드 호출 확인
        self.user_repository.exists_by_email.assert_called_once_with(email)
        self.user_repository.save.assert_called_once()

        # Auth Provider 메서드 호출 확인
        self.auth_provider.create_user.assert_called_once_with(email, password)

    def test_register_fails_when_email_already_exists(self):
        """에러 케이스: 이메일 중복"""
        # Given: 이미 존재하는 이메일
        email = "existing@example.com"
        password = "Password123"

        # Mock 설정
        self.user_repository.exists_by_email.return_value = True

        # When/Then: EmailAlreadyExistsException 발생
        with pytest.raises(EmailAlreadyExistsException):
            self.auth_service.register(email, password)

        # Auth Provider는 호출되지 않음
        self.auth_provider.create_user.assert_not_called()

    def test_register_fails_when_weak_password(self):
        """에러 케이스: 비밀번호 강도 미달"""
        # Given: 약한 비밀번호 (숫자 없음)
        email = "test@example.com"
        password = "Password"  # 숫자 없음

        # Mock 설정
        self.user_repository.exists_by_email.return_value = False

        # When/Then: WeakPasswordException 발생
        with pytest.raises(WeakPasswordException):
            self.auth_service.register(email, password)

        # Auth Provider는 호출되지 않음
        self.auth_provider.create_user.assert_not_called()

    def test_register_fails_when_password_too_short(self):
        """에러 케이스: 비밀번호 너무 짧음"""
        # Given: 7자 비밀번호
        email = "test@example.com"
        password = "Pass12"  # 6자

        # Mock 설정
        self.user_repository.exists_by_email.return_value = False

        # When/Then: WeakPasswordException 발생
        with pytest.raises(WeakPasswordException):
            self.auth_service.register(email, password)
