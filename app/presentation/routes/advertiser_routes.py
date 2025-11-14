"""Advertiser Routes (Flask Blueprint)"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.presentation.forms.advertiser_forms import AdvertiserRegistrationForm
from app.application.services.advertiser_service import AdvertiserService
from app.infrastructure.repositories.advertiser_repository import AdvertiserRepository
from app.infrastructure.repositories.user_repository import UserRepository
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
@login_required
def dashboard():
    """광고주 대시보드 (추후 구현)"""
    return render_template('advertiser/dashboard.html')
