"""Advertiser Routes (Flask Blueprint)"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.presentation.forms.advertiser_forms import AdvertiserRegistrationForm
from app.presentation.forms.campaign_forms import CampaignForm
from app.application.services.advertiser_service import AdvertiserService
from app.application.services.campaign_service import CampaignService
from app.infrastructure.repositories.advertiser_repository import AdvertiserRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.application_repository import ApplicationRepository
from app.infrastructure.repositories.influencer_repository import InfluencerRepository
from app.shared.decorators.auth_decorators import advertiser_required
from app.domain.exceptions.advertiser_exceptions import (
    AdvertiserAlreadyRegisteredException,
    BusinessNumberAlreadyExistsException
)

advertiser_bp = Blueprint('advertiser', __name__, url_prefix='/advertiser')


@advertiser_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_advertiser():
    """
    광고주 정보 등록 페이지

    GET: 등록 폼 표시
    POST: 정보 등록 처리
    """
    form = AdvertiserRegistrationForm()

    if form.validate_on_submit():
        try:
            # Service 인스턴스 생성 (DI)
            advertiser_repo = AdvertiserRepository()
            user_repo = UserRepository()
            advertiser_service = AdvertiserService(advertiser_repo, user_repo)

            # 사업자등록번호에서 하이픈 제거
            business_number_clean = form.business_number.data.replace('-', '')

            # 광고주 정보 등록
            advertiser = advertiser_service.register_advertiser(
                user_id=current_user.id,
                name=form.name.data,
                birth_date=form.birth_date.data,
                phone_number=form.phone_number.data,
                business_name=form.business_name.data,
                address=form.address.data,
                business_phone=form.business_phone.data,
                business_number=business_number_clean,
                representative_name=form.representative_name.data
            )

            flash('광고주 정보가 성공적으로 등록되었습니다!', 'success')
            return redirect(url_for('advertiser.dashboard'))

        except AdvertiserAlreadyRegisteredException as e:
            flash(str(e), 'danger')
        except BusinessNumberAlreadyExistsException as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'광고주 정보 등록 중 오류가 발생했습니다: {str(e)}', 'danger')

    return render_template('advertiser/register.html', form=form)


@advertiser_bp.route('/dashboard')
@advertiser_required
def dashboard():
    """
    광고주 대시보드

    GET: 내 체험단 목록 표시 (모집중, 종료, 완료)
    """
    # Service 인스턴스 생성
    advertiser_repo = AdvertiserRepository()
    campaign_repo = CampaignRepository()
    campaign_service = CampaignService(campaign_repo)

    # 광고주 정보 조회
    advertiser = advertiser_repo.find_by_user_id(current_user.id)

    # 광고주의 체험단 목록 조회
    campaigns = campaign_service.get_advertiser_campaigns(advertiser.id)

    # 상태별로 분류
    recruiting_campaigns = [c for c in campaigns if c.status == 'RECRUITING']
    closed_campaigns = [c for c in campaigns if c.status == 'CLOSED']
    selected_campaigns = [c for c in campaigns if c.status == 'SELECTED']

    return render_template(
        'advertiser/dashboard.html',
        recruiting_campaigns=recruiting_campaigns,
        closed_campaigns=closed_campaigns,
        selected_campaigns=selected_campaigns
    )


@advertiser_bp.route('/campaign/create', methods=['GET', 'POST'])
@advertiser_required
def create_campaign():
    """
    체험단 생성

    GET: 체험단 생성 폼 표시
    POST: 체험단 생성 처리
    """
    form = CampaignForm()

    if form.validate_on_submit():
        try:
            # Service 인스턴스 생성
            advertiser_repo = AdvertiserRepository()
            campaign_repo = CampaignRepository()
            campaign_service = CampaignService(campaign_repo)

            # 광고주 정보 조회
            advertiser = advertiser_repo.find_by_user_id(current_user.id)

            # 이미지 업로드 (기본 구조만 - Supabase Storage 연동은 추후)
            image_url = None
            if form.image.data:
                # TODO: Supabase Storage에 이미지 업로드
                # image_url = storage_service.upload(...)
                pass

            # 체험단 생성
            campaign = campaign_service.create_campaign(
                advertiser_id=advertiser.id,
                title=form.title.data,
                description=form.description.data,
                quota=form.quota.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                benefits=form.benefits.data,
                conditions=form.conditions.data,
                image_url=image_url
            )

            flash('체험단이 성공적으로 생성되었습니다!', 'success')
            return redirect(url_for('advertiser.dashboard'))

        except Exception as e:
            flash(f'체험단 생성 중 오류가 발생했습니다: {str(e)}', 'danger')

    return render_template('advertiser/campaign_create.html', form=form)


@advertiser_bp.route('/campaign/<int:campaign_id>')
@advertiser_required
def campaign_detail(campaign_id: int):
    """
    광고주 체험단 상세 페이지

    GET: 체험단 정보 및 지원자 목록 표시
    """
    from app.extensions import db

    # Service 인스턴스 생성
    advertiser_repo = AdvertiserRepository(db.session)
    campaign_repo = CampaignRepository(db.session)
    application_repo = ApplicationRepository(db.session)
    influencer_repo = InfluencerRepository(db.session)

    campaign_service = CampaignService(
        campaign_repo,
        influencer_repository=influencer_repo,
        application_repository=application_repo
    )

    # 광고주 정보 조회
    advertiser = advertiser_repo.find_by_user_id(current_user.id)

    try:
        # 체험단 정보 조회 (권한 검증 포함)
        applications = campaign_service.get_campaign_applications(
            campaign_id, advertiser.id
        )

        # 체험단 기본 정보 조회
        campaign = campaign_repo.find_by_id(campaign_id)

        return render_template(
            'advertiser/campaign_detail.html',
            campaign=campaign,
            applications=applications
        )

    except Exception as e:
        flash(f'오류가 발생했습니다: {str(e)}', 'danger')
        return redirect(url_for('advertiser.dashboard'))


@advertiser_bp.route('/campaign/<int:campaign_id>/close', methods=['POST'])
@advertiser_required
def close_campaign(campaign_id: int):
    """
    체험단 모집 조기종료

    POST: 모집 종료 처리
    """
    from app.extensions import db

    # Service 인스턴스 생성
    advertiser_repo = AdvertiserRepository(db.session)
    campaign_repo = CampaignRepository(db.session)
    campaign_service = CampaignService(campaign_repo)

    # 광고주 정보 조회
    advertiser = advertiser_repo.find_by_user_id(current_user.id)

    try:
        # 모집 조기종료
        campaign_service.close_campaign_early(campaign_id, advertiser.id)
        flash('체험단 모집이 조기 종료되었습니다.', 'success')

    except Exception as e:
        flash(f'모집 종료 중 오류가 발생했습니다: {str(e)}', 'danger')

    return redirect(url_for('advertiser.campaign_detail', campaign_id=campaign_id))


@advertiser_bp.route('/campaign/<int:campaign_id>/select', methods=['POST'])
@advertiser_required
def select_influencers(campaign_id: int):
    """
    인플루언서 선정

    POST: 선정된 인플루언서 상태 업데이트
    """
    from app.extensions import db
    from app.application.services.application_service import ApplicationService

    # Service 인스턴스 생성
    advertiser_repo = AdvertiserRepository(db.session)
    campaign_repo = CampaignRepository(db.session)
    application_repo = ApplicationRepository(db.session)

    application_service = ApplicationService(application_repo, campaign_repo)

    # 광고주 정보 조회
    advertiser = advertiser_repo.find_by_user_id(current_user.id)

    # 선정된 지원 ID 리스트 가져오기
    selected_ids_str = request.form.getlist('selected_application_ids[]')
    selected_ids = [int(id_str) for id_str in selected_ids_str]

    try:
        # 인플루언서 선정
        application_service.select_influencers(
            campaign_id, advertiser.id, selected_ids
        )
        db.session.commit()
        flash('인플루언서가 성공적으로 선정되었습니다.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'선정 중 오류가 발생했습니다: {str(e)}', 'danger')

    return redirect(url_for('advertiser.campaign_detail', campaign_id=campaign_id))
