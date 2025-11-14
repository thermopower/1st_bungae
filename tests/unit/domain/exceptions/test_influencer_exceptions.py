"""
인플루언서 예외 단위 테스트
"""
import pytest
from app.domain.exceptions.influencer_exceptions import (
    InfluencerAlreadyRegisteredException,
    InfluencerNotFoundException
)
from app.domain.exceptions.base import DomainException


class TestInfluencerExceptions:
    """인플루언서 예외 테스트"""

    def test_influencer_already_registered_exception_is_domain_exception(self):
        """InfluencerAlreadyRegisteredException은 DomainException의 서브클래스"""
        # Assert
        assert issubclass(InfluencerAlreadyRegisteredException, DomainException)

    def test_influencer_already_registered_exception_with_message(self):
        """메시지와 함께 InfluencerAlreadyRegisteredException 생성"""
        # Arrange
        message = "이미 인플루언서로 등록되어 있습니다"

        # Act
        exception = InfluencerAlreadyRegisteredException(message)

        # Assert
        assert str(exception) == message

    def test_influencer_not_found_exception_is_domain_exception(self):
        """InfluencerNotFoundException은 DomainException의 서브클래스"""
        # Assert
        assert issubclass(InfluencerNotFoundException, DomainException)

    def test_influencer_not_found_exception_with_message(self):
        """메시지와 함께 InfluencerNotFoundException 생성"""
        # Arrange
        message = "인플루언서를 찾을 수 없습니다"

        # Act
        exception = InfluencerNotFoundException(message)

        # Assert
        assert str(exception) == message

    def test_influencer_already_registered_exception_can_be_raised(self):
        """InfluencerAlreadyRegisteredException을 raise할 수 있음"""
        # Assert
        with pytest.raises(InfluencerAlreadyRegisteredException) as exc_info:
            raise InfluencerAlreadyRegisteredException("이미 등록됨")

        assert "이미 등록됨" in str(exc_info.value)

    def test_influencer_not_found_exception_can_be_raised(self):
        """InfluencerNotFoundException을 raise할 수 있음"""
        # Assert
        with pytest.raises(InfluencerNotFoundException) as exc_info:
            raise InfluencerNotFoundException("찾을 수 없음")

        assert "찾을 수 없음" in str(exc_info.value)
