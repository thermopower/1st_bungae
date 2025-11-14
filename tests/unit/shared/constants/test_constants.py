"""Constants 테스트"""


class TestUserConstants:
    """User Constants 테스트"""

    def test_user_constants_exist(self):
        """정상 케이스: 상수 존재 확인"""
        from app.shared.constants import user_constants

        assert hasattr(user_constants, "ROLE_ADVERTISER")
        assert hasattr(user_constants, "ROLE_INFLUENCER")
        assert hasattr(user_constants, "VALID_ROLES")
        assert user_constants.ROLE_ADVERTISER == "advertiser"
        assert user_constants.ROLE_INFLUENCER == "influencer"


class TestCampaignConstants:
    """Campaign Constants 테스트"""

    def test_campaign_constants_exist(self):
        """정상 케이스: 상수 존재 확인"""
        from app.shared.constants import campaign_constants

        assert hasattr(campaign_constants, "STATUS_RECRUITING")
        assert hasattr(campaign_constants, "STATUS_CLOSED")
        assert hasattr(campaign_constants, "STATUS_SELECTED")
        assert campaign_constants.STATUS_RECRUITING == "RECRUITING"
        assert campaign_constants.STATUS_CLOSED == "CLOSED"
        assert campaign_constants.STATUS_SELECTED == "SELECTED"
