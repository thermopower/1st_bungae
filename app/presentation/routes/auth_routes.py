"""Auth Routes (회원가입, 로그인)"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, current_user
from app.presentation.forms.auth_forms import RegisterForm, LoginForm
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.external.supabase.supabase_auth import SupabaseAuthProvider
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsException,
    WeakPasswordException,
    InvalidCredentialsException
)
from app.domain.exceptions.validation_exceptions import InvalidEmailException


# Blueprint 생성
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    회원가입 페이지

    GET: 회원가입 폼 표시
    POST: 회원가입 처리
    """
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            from app.extensions import db

            # Service 인스턴스 생성
            user_repository = UserRepository(db.session)
            auth_provider = SupabaseAuthProvider()
            auth_service = AuthService(user_repository, auth_provider)

            print(f"[DEBUG] 회원가입 시도 - Email: {form.email.data}")

            # 회원가입 처리
            response = auth_service.register(
                email=form.email.data,
                password=form.password.data
            )

            print(f"[DEBUG] 회원가입 성공 - User ID: {response.user_id}")
            flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
            return redirect(url_for('auth.login'))

        except EmailAlreadyExistsException as e:
            print(f"[DEBUG] 이메일 중복: {form.email.data}")
            flash('이미 사용 중인 이메일입니다.', 'danger')

        except WeakPasswordException as e:
            print(f"[DEBUG] 비밀번호 강도 미달")
            flash('비밀번호는 최소 8자 이상이며 영문과 숫자를 포함해야 합니다.', 'danger')

        except InvalidEmailException as e:
            print(f"[DEBUG] 이메일 형식 오류: {form.email.data}")
            flash('올바른 이메일 형식이 아닙니다.', 'danger')

        except Exception as e:
            print(f"[ERROR] 회원가입 중 오류 발생: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            flash('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.', 'danger')
    else:
        if request.method == 'POST':
            print(f"[DEBUG] 폼 검증 실패: {form.errors}")

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    로그인 페이지

    GET: 로그인 폼 표시
    POST: 로그인 처리
    """
    # 이미 로그인된 사용자는 홈으로 리다이렉트
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        try:
            from app.extensions import db

            # Service 인스턴스 생성
            user_repository = UserRepository(db.session)
            auth_provider = SupabaseAuthProvider()
            auth_service = AuthService(user_repository, auth_provider)

            # 로그인 처리
            response = auth_service.login(
                email=form.email.data,
                password=form.password.data
            )

            # 세션에 토큰 저장
            session['access_token'] = response.access_token
            session['refresh_token'] = response.refresh_token
            session['user_id'] = response.user_id

            # Flask-Login 세션 설정
            from app.infrastructure.persistence.models.user_model import UserModel
            user_model = UserModel.query.get(response.user_id)
            if user_model:
                login_user(user_model)

            flash('로그인에 성공했습니다!', 'success')
            return redirect(response.redirect_url)

        except InvalidCredentialsException:
            flash('이메일 또는 비밀번호가 일치하지 않습니다.', 'danger')

        except InvalidEmailException:
            flash('올바른 이메일 형식이 아닙니다.', 'danger')

        except Exception as e:
            flash('로그인 중 오류가 발생했습니다. 다시 시도해주세요.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """로그아웃"""
    logout_user()
    session.clear()
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('auth.login'))
