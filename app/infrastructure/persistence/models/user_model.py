"""User ORM Model (데이터베이스 테이블)"""

from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime, UTC


class UserModel(db.Model, UserMixin):
    """
    사용자 ORM 모델 (users 테이블)

    Supabase Auth와 연동되는 사용자 인증 정보 저장
    Flask-Login의 UserMixin을 상속하여 로그인 세션 관리 지원
    """

    __tablename__ = 'users'

    # 기본키: UUID (Supabase Auth에서 생성)
    id = db.Column(db.String(36), primary_key=True)

    # 이메일 (Supabase Auth에서 관리)
    email = db.Column(db.String(255), unique=True, nullable=False)

    # 사용자 역할 (advertiser/influencer/None)
    role = db.Column(db.String(20), nullable=True)

    # 계정 생성일
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    # 관계
    # advertiser = db.relationship('AdvertiserModel', back_populates='user', uselist=False, cascade='all, delete-orphan')
    # influencer = db.relationship('InfluencerModel', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<UserModel id={self.id} email={self.email} role={self.role}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user_loader 콜백"""
    return UserModel.query.get(user_id)
