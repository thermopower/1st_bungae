"""Main Routes (홈 페이지 등)"""

from flask import Blueprint, render_template, request

from app.application.services.campaign_service import CampaignService
from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.extensions import db


# Blueprint 생성
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """
    홈 페이지 - 체험단 탐색

    GET 파라미터:
    - page: 페이지 번호 (기본값: 1)
    - sort: 정렬 기준 (latest, deadline, popular)

    Returns:
        홈 페이지 HTML
    """
    # Query 파라미터 파싱
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'latest', type=str)

    # 의존성 주입
    campaign_repository = CampaignRepository(db.session)
    campaign_service = CampaignService(campaign_repository)

    # 모집 중인 체험단 목록 조회
    campaigns, total_count = campaign_service.list_recruiting_campaigns(
        page=page, per_page=12, sort=sort
    )

    # 총 페이지 수 계산
    total_pages = (total_count + 11) // 12  # ceil(total_count / 12)

    return render_template(
        'home.html',
        campaigns=campaigns,
        current_page=page,
        total_pages=total_pages,
        total_count=total_count,
        sort=sort
    )
