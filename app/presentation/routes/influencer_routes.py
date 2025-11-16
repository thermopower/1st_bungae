# -*- coding: utf-8 -*-
"""
Influencer Routes (Flask Blueprint)
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.presentation.forms.influencer_forms import InfluencerRegistrationForm
from app.application.services.influencer_service import InfluencerService
from app.application.services.application_service import ApplicationService
from app.infrastructure.repositories.influencer_repository import InfluencerRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.application_repository import ApplicationRepository
from app.infrastructure.repositories.campaign_repository import CampaignRepository
from app.infrastructure.repositories.advertiser_repository import AdvertiserRepository
from app.domain.exceptions.influencer_exceptions import (
    InfluencerAlreadyRegisteredException,
    InfluencerNotFoundException
)
from app.shared.decorators.auth_decorators import influencer_required
import json

influencer_bp = Blueprint('influencer', __name__, url_prefix='/influencer')


@influencer_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_influencer():
    """
    인플루언서 정보 등록 페이지

    GET: 등록 폼 표시
    POST: 정보 등록 처리
    """
    form = InfluencerRegistrationForm()

    if form.validate_on_submit():
        try:
            from app.extensions import db

            # Service 인스턴스 생성 (DI)
            influencer_repo = InfluencerRepository(db.session)
            user_repo = UserRepository(db.session)
            influencer_service = InfluencerService(influencer_repo, user_repo)

            # 채널 타입은 현재 DB에 저장하지 않음 (향후 확장 가능)
            # channel_type = form.channel_type.data

            # 인플루언서 정보 등록
            influencer = influencer_service.register_influencer(
                user_id=current_user.id,
                name=form.name.data,
                birth_date=form.birth_date.data,
                phone_number=form.phone_number.data,
                channel_name=form.channel_name.data,
                channel_url=form.channel_url.data,
                follower_count=form.follower_count.data
            )

            flash('인플루언서 정보가 성공적으로 등록되었습니다!', 'success')
            return redirect(url_for('main.home'))

        except InfluencerAlreadyRegisteredException as e:
            flash(str(e), 'danger')
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'인플루언서 정보 등록 중 오류가 발생했습니다: {str(e)}', 'danger')

    return render_template('influencer/register.html', form=form)


@influencer_bp.route('/applications', methods=['GET'])
@influencer_required
def applications():
    """
    인플루언서 지원 내역 조회 페이지

    Returns:
        지원 내역 목록 페이지 (applications.html)
    """
    try:
        from app.extensions import db

        # Repository 및 Service 생성 (DI)
        application_repo = ApplicationRepository(db.session)
        campaign_repo = CampaignRepository(db.session)
        influencer_repo = InfluencerRepository(db.session)
        advertiser_repo = AdvertiserRepository(db.session)

        application_service = ApplicationService(
            application_repo,
            campaign_repo,
            influencer_repo
        )

        # 현재 인플루언서 ID 조회
        influencer = influencer_repo.find_by_user_id(current_user.id)
        if influencer is None:
            flash('인플루언서 정보를 먼저 등록해주세요.', 'warning')
            return redirect(url_for('influencer.register_influencer'))

        # 지원 내역 조회
        applications_list = application_service.get_applications_by_influencer(influencer.id)

        # 각 지원 내역에 Campaign 및 Advertiser 정보 추가
        enriched_applications = []
        for app in applications_list:
            campaign = campaign_repo.find_by_id(app.campaign_id)
            if campaign:
                advertiser = advertiser_repo.find_by_id(campaign.advertiser_id)

                enriched_applications.append({
                    'id': app.id,
                    'status': app.status,
                    'status_text': STATUS_TEXT_MAP.get(app.status, app.status),
                    'status_badge_color': STATUS_BADGE_COLOR_MAP.get(app.status, 'secondary'),
                    'applied_at': app.applied_at,
                    'campaign': {
                        'id': campaign.id,
                        'title': campaign.title,
                        'end_date': campaign.end_date,
                        'status': campaign.status
                    },
                    'advertiser': {
                        'business_name': advertiser.business_name if advertiser else '알 수 없음'
                    }
                })

        # 상태별 개수 계산
        status_counts = {
            'applied': sum(1 for app in applications_list if app.is_applied()),
            'selected': sum(1 for app in applications_list if app.is_selected()),
            'rejected': sum(1 for app in applications_list if app.is_rejected())
        }

        # JavaScript용 JSON 생성
        applications_json = json.dumps([
            {
                'id': app['id'],
                'status': app['status'],
                'applied_at': app['applied_at'].isoformat(),
            }
            for app in enriched_applications
        ], ensure_ascii=False)

        return render_template(
            'influencer/applications.html',
            applications=enriched_applications,
            status_counts=status_counts,
            total_count=len(applications_list),
            applications_json=applications_json
        )

    except InfluencerNotFoundException as e:
        flash(str(e), 'danger')
        return redirect(url_for('influencer.register_influencer'))
    except Exception as e:
        flash(f'지원 내역을 불러오는 중 오류가 발생했습니다: {str(e)}', 'danger')
        return redirect(url_for('main.home'))


# 상수 정의
STATUS_TEXT_MAP = {
    'APPLIED': '지원완료',
    'SELECTED': '선정됨',
    'REJECTED': '탈락'
}

STATUS_BADGE_COLOR_MAP = {
    'APPLIED': 'primary',
    'SELECTED': 'success',
    'REJECTED': 'secondary'
}
