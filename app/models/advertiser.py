"""
광고주 모델
"""
from app.extensions import db
from datetime import datetime


class Advertiser(db.Model):
    """광고주 정보"""

    __tablename__ = 'advertisers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # 광고주 상세 정보
    company_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    company_phone = db.Column(db.String(20), nullable=False)
    business_number = db.Column(db.String(50), nullable=False, unique=True)
    ceo_name = db.Column(db.String(100), nullable=False)

    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    campaigns = db.relationship('Campaign', backref='advertiser', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Advertiser {self.company_name}>'
