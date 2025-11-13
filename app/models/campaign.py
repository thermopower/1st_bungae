"""
체험단 캠페인 모델
"""
from app.extensions import db
from datetime import datetime


class Campaign(db.Model):
    """체험단 캠페인"""

    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertisers.id'), nullable=False)

    # 캠페인 기본 정보
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)

    # 모집 정보
    recruit_count = db.Column(db.Integer, nullable=False)  # 모집 인원
    start_date = db.Column(db.Date, nullable=False)  # 시작일
    end_date = db.Column(db.Date, nullable=False)  # 종료일

    # 상태 관리
    status = db.Column(db.String(20), default='recruiting')  # recruiting, closed, completed
    is_early_closed = db.Column(db.Boolean, default=False)  # 조기 종료 여부

    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    applications = db.relationship('Application', backref='campaign', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Campaign {self.title}>'
