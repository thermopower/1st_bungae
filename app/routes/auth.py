"""
인증 관련 라우트
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """로그인"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # TODO: Supabase Auth 연동
        flash('로그인 기능은 Supabase Auth 연동 후 구현됩니다.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # TODO: Supabase Auth 연동
        flash('회원가입 기능은 Supabase Auth 연동 후 구현됩니다.', 'info')
        return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@bp.route('/logout')
def logout():
    """로그아웃"""
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/profile/type', methods=['GET', 'POST'])
def select_profile_type():
    """프로필 타입 선택 (광고주/인플루언서)"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        profile_type = request.form.get('profile_type')
        if profile_type == 'advertiser':
            return redirect(url_for('advertiser.register'))
        elif profile_type == 'influencer':
            return redirect(url_for('influencer.register'))

    return render_template('auth/select_profile_type.html')
