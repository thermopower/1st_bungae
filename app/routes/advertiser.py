"""
광고주 관련 라우트
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.advertiser import Advertiser
from app.models.campaign import Campaign
from app.extensions import db

bp = Blueprint('advertiser', __name__, url_prefix='/advertiser')


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """광고주 정보 등록"""
    if current_user.advertiser_profile:
        flash('이미 광고주 정보가 등록되어 있습니다.', 'info')
        return redirect(url_for('advertiser.dashboard'))

    if request.method == 'POST':
        # TODO: 폼 데이터 검증 및 저장
        flash('광고주 정보 등록 기능은 구현 예정입니다.', 'info')
        return redirect(url_for('advertiser.register'))

    return render_template('advertiser/register.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    """광고주 대시보드"""
    if not current_user.advertiser_profile:
        flash('광고주 정보를 먼저 등록해주세요.', 'warning')
        return redirect(url_for('advertiser.register'))

    campaigns = Campaign.query.filter_by(
        advertiser_id=current_user.advertiser_profile.id
    ).order_by(Campaign.created_at.desc()).all()

    return render_template('advertiser/dashboard.html', campaigns=campaigns)


@bp.route('/campaign/<int:campaign_id>')
@login_required
def campaign_detail(campaign_id):
    """체험단 관리 상세"""
    if not current_user.advertiser_profile:
        flash('권한이 없습니다.', 'danger')
        return redirect(url_for('main.index'))

    campaign = Campaign.query.get_or_404(campaign_id)

    # 본인의 캠페인인지 확인
    if campaign.advertiser_id != current_user.advertiser_profile.id:
        flash('권한이 없습니다.', 'danger')
        return redirect(url_for('advertiser.dashboard'))

    return render_template('advertiser/campaign_detail.html', campaign=campaign)


@bp.route('/campaign/<int:campaign_id>/close', methods=['POST'])
@login_required
def close_campaign(campaign_id):
    """캠페인 조기 종료"""
    if not current_user.advertiser_profile:
        flash('권한이 없습니다.', 'danger')
        return redirect(url_for('main.index'))

    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.advertiser_id != current_user.advertiser_profile.id:
        flash('권한이 없습니다.', 'danger')
        return redirect(url_for('advertiser.dashboard'))

    campaign.status = 'closed'
    campaign.is_early_closed = True
    db.session.commit()

    flash('캠페인이 조기 종료되었습니다.', 'success')
    return redirect(url_for('advertiser.campaign_detail', campaign_id=campaign_id))
