"""
Influencer Routes (Flask Blueprint)
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.presentation.forms.influencer_forms import InfluencerRegistrationForm
from app.application.services.influencer_service import InfluencerService
from app.infrastructure.repositories.influencer_repository import InfluencerRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.exceptions.influencer_exceptions import (
    InfluencerAlreadyRegisteredException,
    InfluencerNotFoundException
)

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
            # Service 인스턴스 생성 (DI)
            influencer_repo = InfluencerRepository()
            user_repo = UserRepository()
            influencer_service = InfluencerService(influencer_repo, user_repo)

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
