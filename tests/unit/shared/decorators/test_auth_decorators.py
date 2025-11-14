"""
@advertiser_required, @influencer_required 데코레이터 단위 테스트
"""

import pytest
from app.shared.decorators.auth_decorators import advertiser_required, influencer_required


# ===========================
# 데코레이터 함수 존재 여부 테스트
# ===========================

def test_advertiser_required_decorator_exists():
    """
    @advertiser_required 데코레이터가 정의되어 있는지 확인
    """
    assert callable(advertiser_required)


def test_influencer_required_decorator_exists():
    """
    @influencer_required 데코레이터가 정의되어 있는지 확인
    """
    assert callable(influencer_required)


def test_advertiser_required_decorator_wraps_function():
    """
    @advertiser_required 데코레이터가 함수를 감싸는지 확인
    """
    @advertiser_required
    def dummy_function():
        return "Hello"

    # 함수가 정상적으로 감싸졌는지 확인
    assert callable(dummy_function)
    assert dummy_function.__name__ == "dummy_function"


def test_influencer_required_decorator_wraps_function():
    """
    @influencer_required 데코레이터가 함수를 감싸는지 확인
    """
    @influencer_required
    def dummy_function():
        return "Hello"

    # 함수가 정상적으로 감싸졌는지 확인
    assert callable(dummy_function)
    assert dummy_function.__name__ == "dummy_function"


# ===========================
# 실제 권한 검증 로직은 E2E 테스트에서 수행
# ===========================
# E2E 테스트에서:
# 1. 로그인하지 않은 사용자가 @advertiser_required 라우트 접근 시 리다이렉트
# 2. 광고주 정보 미등록 사용자가 접근 시 /advertiser/register로 리다이렉트
# 3. 광고주 정보 등록 사용자가 접근 시 정상 접근
