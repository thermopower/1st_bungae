"""
Application Entity 단위 테스트
"""

import pytest
from datetime import datetime
from app.domain.entities.application import Application
from app.shared.constants.campaign_constants import (
    APPLICATION_STATUS_APPLIED,
    APPLICATION_STATUS_SELECTED,
    APPLICATION_STATUS_REJECTED,
)


class TestApplicationEntity:
    """Application 엔티티 단위 테스트"""

    def test_create_application_with_required_fields(self):
        """필수 필드로 Application 생성 시 정상 생성"""
        # Arrange & Act
        application = Application(
            id=None,
            campaign_id=1,
            influencer_id=1,
            application_reason="테스트 지원 사유입니다.",
            status=APPLICATION_STATUS_APPLIED,
            applied_at=datetime.now()
        )

        # Assert
        assert application.id is None
        assert application.campaign_id == 1
        assert application.influencer_id == 1
        assert application.application_reason == "테스트 지원 사유입니다."
        assert application.status == APPLICATION_STATUS_APPLIED
        assert isinstance(application.applied_at, datetime)

    def test_create_application_without_reason(self):
        """지원 사유 없이 Application 생성 시 정상 생성 (선택 필드)"""
        # Arrange & Act
        application = Application(
            id=None,
            campaign_id=1,
            influencer_id=1,
            application_reason=None,
            status=APPLICATION_STATUS_APPLIED,
            applied_at=datetime.now()
        )

        # Assert
        assert application.application_reason is None

    def test_is_applied_returns_true_when_status_is_applied(self):
        """status가 APPLIED일 때 is_applied()가 True 반환"""
        # Arrange
        application = Application(
            id=1,
            campaign_id=1,
            influencer_id=1,
            application_reason=None,
            status=APPLICATION_STATUS_APPLIED,
            applied_at=datetime.now()
        )

        # Act & Assert
        assert application.is_applied() is True

    def test_is_applied_returns_false_when_status_is_selected(self):
        """status가 SELECTED일 때 is_applied()가 False 반환"""
        # Arrange
        application = Application(
            id=1,
            campaign_id=1,
            influencer_id=1,
            application_reason=None,
            status=APPLICATION_STATUS_SELECTED,
            applied_at=datetime.now()
        )

        # Act & Assert
        assert application.is_applied() is False

    def test_is_selected_returns_true_when_status_is_selected(self):
        """status가 SELECTED일 때 is_selected()가 True 반환"""
        # Arrange
        application = Application(
            id=1,
            campaign_id=1,
            influencer_id=1,
            application_reason=None,
            status=APPLICATION_STATUS_SELECTED,
            applied_at=datetime.now()
        )

        # Act & Assert
        assert application.is_selected() is True

    def test_is_rejected_returns_true_when_status_is_rejected(self):
        """status가 REJECTED일 때 is_rejected()가 True 반환"""
        # Arrange
        application = Application(
            id=1,
            campaign_id=1,
            influencer_id=1,
            application_reason=None,
            status=APPLICATION_STATUS_REJECTED,
            applied_at=datetime.now()
        )

        # Act & Assert
        assert application.is_rejected() is True
