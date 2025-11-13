"""
인플루언서 모델
"""
from app.extensions import db
from datetime import datetime


class Influencer(db.Model):
    """인플루언서 정보"""

    __tablename__ = 'influencers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # 인플루언서 상세 정보
    channel_name = db.Column(db.String(200), nullable=False)
    channel_url = db.Column(db.String(300), nullable=False)
    follower_count = db.Column(db.Integer, nullable=False)

    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    applications = db.relationship('Application', backref='influencer', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Influencer {self.channel_name}>'
