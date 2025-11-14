# app/presentation/routes/campaign_routes.py
"""
Campaign Routes
체험단 관련 라우트
"""

from flask import Blueprint, render_template, session, abort

from app.application.services.campaign_service import CampaignService
from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.influencer_repository import InfluencerRepository
from app.infrastructure.repositories.application_repository import ApplicationRepository
from app.extensions import db


# Blueprint 생성
campaign_bp = Blueprint('campaign', __name__, url_prefix='/campaign')


@campaign_bp.route('/<int:campaign_id>')
def campaign_detail(campaign_id: int):
    """
    체험단 상세 페이지

    GET: 체험단 정보 및 광고주 정보 표시

    Args:
        campaign_id: 체험단 ID

    Returns:
        체험단 상세 HTML 페이지
    """
    # 의존성 주입 (간소화를 위해 여기서 생성, 추후 DI 컨테이너 사용 가능)
    campaign_repository = CampaignRepository(db.session)
    influencer_repository = InfluencerRepository(db.session)
    application_repository = ApplicationRepository(db.session)

    campaign_service = CampaignService(
        campaign_repository=campaign_repository,
        influencer_repository=influencer_repository,
        application_repository=application_repository
    )

    # 현재 로그인한 사용자 ID 가져오기 (session)
    user_id = session.get('user_id')

    # 체험단 상세 조회
    campaign = campaign_service.get_campaign_detail(campaign_id, user_id)

    if campaign is None:
        abort(404, description="체험단을 찾을 수 없습니다.")

    return render_template('campaign/detail.html', campaign=campaign)
