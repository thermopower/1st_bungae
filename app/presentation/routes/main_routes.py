"""Main Routes (홈 페이지 등)"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.application.services.campaign_service import CampaignService
from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.user_repository import UserRepository
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


@main_bp.route('/role-selection', methods=['GET', 'POST'])
@login_required
def role_selection():
    """
    역할 선택 페이지

    GET: 역할 선택 페이지 표시
    POST: 선택한 역할 저장 및 리다이렉트
    """
    # 이미 역할이 있는 경우 해당 페이지로 리다이렉트
    if current_user.role:
        if current_user.role == 'advertiser':
            return redirect(url_for('advertiser.dashboard'))
        elif current_user.role == 'influencer':
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        role = request.form.get('role')

        if role not in ['advertiser', 'influencer']:
            flash('올바른 역할을 선택해주세요.', 'danger')
            return render_template('role_selection.html')

        # 역할 저장
        from app.extensions import db
        user_repository = UserRepository(db.session)
        user = user_repository.find_by_id(current_user.id)
        if user:
            user.role = role
            user_repository.save(user)

            flash(f'{"광고주" if role == "advertiser" else "인플루언서"}로 등록되었습니다!', 'success')

            # 역할에 따라 리다이렉트
            if role == 'advertiser':
                return redirect(url_for('advertiser.register_advertiser'))
            else:
                return redirect(url_for('influencer.register_influencer'))
        else:
            flash('사용자 정보를 찾을 수 없습니다.', 'danger')

    return render_template('role_selection.html')
