"""Advertiser 도메인 예외 테스트"""

import pytest
from app.domain.exceptions.advertiser_exceptions import (
    AdvertiserAlreadyRegisteredException,
    BusinessNumberAlreadyExistsException
)
from app.domain.exceptions.base import DomainException


class TestAdvertiserExceptions:
    """광고주 도메인 예외 테스트"""

    def test_advertiser_already_registered_exception_inherits_from_domain_exception(self):
        """AdvertiserAlreadyRegisteredException이 DomainException을 상속하는지 확인"""
        # Arrange & Act
        exception = AdvertiserAlreadyRegisteredException("이미 광고주로 등록되었습니다")

        # Assert
        assert isinstance(exception, DomainException)
        assert str(exception) == "이미 광고주로 등록되었습니다"

    def test_business_number_already_exists_exception_inherits_from_domain_exception(self):
        """BusinessNumberAlreadyExistsException이 DomainException을 상속하는지 확인"""
        # Arrange & Act
        exception = BusinessNumberAlreadyExistsException("사업자등록번호 1234567890이 이미 존재합니다")

        # Assert
        assert isinstance(exception, DomainException)
        assert str(exception) == "사업자등록번호 1234567890이 이미 존재합니다"

    def test_advertiser_already_registered_exception_can_be_raised(self):
        """AdvertiserAlreadyRegisteredException을 발생시킬 수 있는지 확인"""
        # Arrange & Act & Assert
        with pytest.raises(AdvertiserAlreadyRegisteredException) as exc_info:
            raise AdvertiserAlreadyRegisteredException("이미 등록됨")

        assert "이미 등록됨" in str(exc_info.value)

    def test_business_number_already_exists_exception_can_be_raised(self):
        """BusinessNumberAlreadyExistsException을 발생시킬 수 있는지 확인"""
        # Arrange & Act & Assert
        with pytest.raises(BusinessNumberAlreadyExistsException) as exc_info:
            raise BusinessNumberAlreadyExistsException("중복된 사업자등록번호")

        assert "중복된 사업자등록번호" in str(exc_info.value)
