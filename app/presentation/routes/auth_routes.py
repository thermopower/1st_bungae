"""Auth Routes (회원가입, 로그인)"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.presentation.forms.auth_forms import RegisterForm
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.external.supabase.supabase_auth import SupabaseAuthProvider
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsException,
    WeakPasswordException
)
from app.domain.exceptions.validation_exceptions import InvalidEmailException


# Blueprint 생성
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 의존성 주입 (추후 Flask 앱 팩토리에서 처리)
user_repository = UserRepository()
auth_provider = SupabaseAuthProvider()
auth_service = AuthService(user_repository, auth_provider)


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
            # 회원가입 처리
            response = auth_service.register(
                email=form.email.data,
                password=form.password.data
            )

            flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
            return redirect(url_for('auth.login'))

        except EmailAlreadyExistsException:
            flash('이미 사용 중인 이메일입니다.', 'danger')

        except WeakPasswordException:
            flash('비밀번호는 최소 8자 이상이며 영문과 숫자를 포함해야 합니다.', 'danger')

        except InvalidEmailException:
            flash('올바른 이메일 형식이 아닙니다.', 'danger')

        except Exception as e:
            flash('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.', 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """로그인 페이지 (추후 구현)"""
    return "로그인 페이지"
