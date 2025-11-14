"""간단한 로그인 관련 테스트 (Flask 없이)"""

import sys
import io

# Windows에서 UTF-8 출력 보장
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime, UTC
from dataclasses import dataclass
from typing import Optional


# 간단한 Email Value Object
@dataclass(frozen=True)
class Email:
    value: str


# 간단한 User Entity
@dataclass
class User:
    id: str
    email: Email
    role: Optional[str]
    created_at: datetime

    def has_role(self) -> bool:
        return self.role is not None


# UserRules determine_redirect_url 메서드 테스트
class UserRules:
    @staticmethod
    def determine_redirect_url(user: User) -> str:
        """
        사용자 역할에 따른 리다이렉트 URL 결정

        Args:
            user: User 엔티티

        Returns:
            str: 리다이렉트 URL

        Raises:
            ValueError: 알 수 없는 역할
        """
        if not user.has_role():
            return '/role-selection'
        elif user.role == 'advertiser':
            return '/advertiser/dashboard'
        elif user.role == 'influencer':
            return '/'
        else:
            raise ValueError(f"Unknown role: {user.role}")


# 테스트
def test_determine_redirect_url():
    # 테스트 1: 역할이 없는 사용자
    user1 = User(
        id="test-1",
        email=Email("test1@example.com"),
        role=None,
        created_at=datetime.now(UTC)
    )
    assert UserRules.determine_redirect_url(user1) == '/role-selection'
    print("✅ 테스트 1 통과: 역할 없음 -> /role-selection")

    # 테스트 2: 광고주
    user2 = User(
        id="test-2",
        email=Email("advertiser@example.com"),
        role='advertiser',
        created_at=datetime.now(UTC)
    )
    assert UserRules.determine_redirect_url(user2) == '/advertiser/dashboard'
    print("✅ 테스트 2 통과: advertiser -> /advertiser/dashboard")

    # 테스트 3: 인플루언서
    user3 = User(
        id="test-3",
        email=Email("influencer@example.com"),
        role='influencer',
        created_at=datetime.now(UTC)
    )
    assert UserRules.determine_redirect_url(user3) == '/'
    print("✅ 테스트 3 통과: influencer -> /")

    # 테스트 4: 알 수 없는 역할
    user4 = User(
        id="test-4",
        email=Email("admin@example.com"),
        role='admin',
        created_at=datetime.now(UTC)
    )
    try:
        UserRules.determine_redirect_url(user4)
        assert False, "ValueError가 발생해야 합니다"
    except ValueError as e:
        assert "Unknown role" in str(e)
        print("✅ 테스트 4 통과: 알 수 없는 역할 -> ValueError")

    print("\n✅ 모든 테스트 통과! 이제 실제 코드에 적용합니다.\n")


if __name__ == '__main__':
    test_determine_redirect_url()
