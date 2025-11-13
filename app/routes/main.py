"""
메인 페이지 라우트
"""
from flask import Blueprint, render_template
from app.models.campaign import Campaign

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """홈 - 체험단 탐색"""
    campaigns = Campaign.query.filter_by(status='recruiting').order_by(Campaign.created_at.desc()).all()
    return render_template('index.html', campaigns=campaigns)


@bp.route('/campaign/<int:campaign_id>')
def campaign_detail(campaign_id):
    """체험단 상세"""
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign_detail.html', campaign=campaign)
