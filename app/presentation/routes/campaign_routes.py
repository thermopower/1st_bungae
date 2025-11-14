# app/presentation/routes/campaign_routes.py
"""
Campaign Routes
체험단 관련 라우트
"""

from flask import Blueprint, render_template, session, abort, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app.application.services.campaign_service import CampaignService
from app.application.services.application_service import ApplicationService
from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.influencer_repository import InfluencerRepository
from app.infrastructure.repositories.application_repository import ApplicationRepository
from app.extensions import db
from app.presentation.forms.campaign_forms import CampaignApplicationForm
from app.shared.decorators.auth_decorators import influencer_required
from app.domain.exceptions.application_exceptions import (
    AlreadyAppliedException,
    CampaignNotRecruitingException,
    InfluencerNotRegisteredException,
)
from app.domain.exceptions.campaign_exceptions import CampaignNotFoundException


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


@campaign_bp.route('/<int:campaign_id>/apply', methods=['GET', 'POST'])
@login_required
@influencer_required
def apply_campaign(campaign_id: int):
    """
    체험단 지원 페이지

    GET: 지원 폼 표시
    POST: 지원 처리

    Args:
        campaign_id: 체험단 ID

    Returns:
        GET: 지원 폼 HTML 페이지
        POST: 체험단 상세 페이지로 리다이렉트
    """
    # Form 생성
    form = CampaignApplicationForm()

    # 의존성 주입
    campaign_repository = CampaignRepository(db.session)
    influencer_repository = InfluencerRepository(db.session)
    application_repository = ApplicationRepository(db.session)

    campaign_service = CampaignService(
        campaign_repository=campaign_repository,
        influencer_repository=influencer_repository,
        application_repository=application_repository
    )

    application_service = ApplicationService(
        application_repository=application_repository,
        campaign_repository=campaign_repository,
        influencer_repository=influencer_repository
    )

    # 체험단 정보 조회
    campaign = campaign_service.get_campaign_detail(campaign_id, current_user.id)
    if campaign is None:
        abort(404, description="체험단을 찾을 수 없습니다.")

    # 인플루언서 정보 조회
    influencer = influencer_repository.find_by_user_id(current_user.id)
    if influencer is None:
        flash('인플루언서 정보를 먼저 등록해주세요.', 'warning')
        return redirect(url_for('influencer.register_influencer', next=request.url))

    if form.validate_on_submit():
        # POST 요청 처리
        try:
            application_service.apply_to_campaign(
                campaign_id=campaign_id,
                influencer_id=influencer.id,
                application_reason=form.application_reason.data
            )

            db.session.commit()
            flash('체험단 지원이 완료되었습니다!', 'success')
            return redirect(url_for('campaign.campaign_detail', campaign_id=campaign_id))

        except AlreadyAppliedException as e:
            db.session.rollback()
            flash(str(e), 'danger')
            return redirect(url_for('campaign.campaign_detail', campaign_id=campaign_id))

        except CampaignNotRecruitingException as e:
            db.session.rollback()
            flash(str(e), 'danger')
            return redirect(url_for('campaign.campaign_detail', campaign_id=campaign_id))

        except CampaignNotFoundException as e:
            db.session.rollback()
            abort(404, description=str(e))

        except Exception as e:
            db.session.rollback()
            flash(f'지원 처리 중 오류가 발생했습니다: {str(e)}', 'danger')
            return redirect(url_for('campaign.campaign_detail', campaign_id=campaign_id))

    # GET 요청: 폼 표시
    return render_template(
        'campaign/apply.html',
        form=form,
        campaign=campaign
    )
