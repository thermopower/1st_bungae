"""
사용자 모델
"""
from flask_login import UserMixin
from app.extensions import db
from datetime import datetime


class User(UserMixin, db.Model):
    """사용자 기본 정보"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # 계정 유형 (advertiser, influencer)
    account_type = db.Column(db.String(20))

    # Supabase Auth 연동
    supabase_uid = db.Column(db.String(100), unique=True, index=True)

    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    advertiser_profile = db.relationship('Advertiser', backref='user', uselist=False, cascade='all, delete-orphan')
    influencer_profile = db.relationship('Influencer', backref='user', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'
