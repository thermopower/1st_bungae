"""
권한 관리 데코레이터
광고주/인플루언서 권한 검증
"""

from functools import wraps
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.infrastructure.repositories.advertiser_repository import AdvertiserRepository
from app.infrastructure.repositories.influencer_repository import InfluencerRepository


def advertiser_required(f):
    """
    광고주 권한 검증 데코레이터

    - 로그인 필수
    - Advertiser 정보 등록 필수
    - 미등록 시 advertiser.register_advertiser로 리다이렉트

    Usage:
        @advertiser_bp.route('/dashboard')
        @advertiser_required
        def dashboard():
            return render_template('advertiser/dashboard.html')
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # 사용자 ID 가져오기
        user_id = current_user.id

        # Advertiser 정보 조회
        advertiser_repo = AdvertiserRepository()
        advertiser = advertiser_repo.find_by_user_id(user_id)

        if not advertiser:
            # 광고주 정보 미등록
            flash('광고주 정보를 먼저 등록해주세요.', 'warning')
            return redirect(url_for('advertiser.register_advertiser', next=request.url))

        # 정상적으로 라우트 함수 실행
        return f(*args, **kwargs)

    return decorated_function


def influencer_required(f):
    """
    인플루언서 권한 검증 데코레이터

    - 로그인 필수
    - Influencer 정보 등록 필수
    - 미등록 시 influencer.register_influencer로 리다이렉트

    Usage:
        @influencer_bp.route('/profile')
        @influencer_required
        def profile():
            return render_template('influencer/profile.html')
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # 사용자 ID 가져오기
        user_id = current_user.id

        # Influencer 정보 조회
        influencer_repo = InfluencerRepository()
        influencer = influencer_repo.find_by_user_id(user_id)

        if not influencer:
            # 인플루언서 정보 미등록
            flash('인플루언서 정보를 먼저 등록해주세요.', 'warning')
            return redirect(url_for('influencer.register_influencer', next=request.url))

        # 정상적으로 라우트 함수 실행
        return f(*args, **kwargs)

    return decorated_function
