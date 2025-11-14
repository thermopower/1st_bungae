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
