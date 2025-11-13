"""
인플루언서 관련 라우트
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.influencer import Influencer
from app.models.application import Application
from app.models.campaign import Campaign
from app.extensions import db

bp = Blueprint('influencer', __name__, url_prefix='/influencer')


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """인플루언서 정보 등록"""
    if current_user.influencer_profile:
        flash('이미 인플루언서 정보가 등록되어 있습니다.', 'info')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # TODO: 폼 데이터 검증 및 저장
        flash('인플루언서 정보 등록 기능은 구현 예정입니다.', 'info')
        return redirect(url_for('influencer.register'))

    return render_template('influencer/register.html')


@bp.route('/campaign/<int:campaign_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_campaign(campaign_id):
    """체험단 지원"""
    if not current_user.influencer_profile:
        flash('인플루언서 정보를 먼저 등록해주세요.', 'warning')
        return redirect(url_for('influencer.register'))

    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.status != 'recruiting':
        flash('모집이 종료된 체험단입니다.', 'warning')
        return redirect(url_for('main.campaign_detail', campaign_id=campaign_id))

    # 이미 지원했는지 확인
    existing_application = Application.query.filter_by(
        campaign_id=campaign_id,
        influencer_id=current_user.influencer_profile.id
    ).first()

    if existing_application:
        flash('이미 지원한 체험단입니다.', 'info')
        return redirect(url_for('main.campaign_detail', campaign_id=campaign_id))

    if request.method == 'POST':
        message = request.form.get('message', '')

        application = Application(
            campaign_id=campaign_id,
            influencer_id=current_user.influencer_profile.id,
            message=message
        )

        db.session.add(application)
        db.session.commit()

        flash('체험단 지원이 완료되었습니다.', 'success')
        return redirect(url_for('main.campaign_detail', campaign_id=campaign_id))

    return render_template('influencer/apply.html', campaign=campaign)
