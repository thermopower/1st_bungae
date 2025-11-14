# app/infrastructure/persistence/models/campaign_model.py
"""
Campaign ORM Model (데이터베이스 테이블)
"""

from app.extensions import db
from datetime import datetime, UTC, date


class CampaignModel(db.Model):
    """
    체험단 ORM 모델 (campaign 테이블)

    광고주가 생성한 체험단 정보 저장
    """

    __tablename__ = 'campaign'

    # 기본키
    id = db.Column(db.Integer, primary_key=True)

    # 외래키: Advertiser
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'), nullable=False)

    # 체험단 정보
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quota = db.Column(db.Integer, nullable=False)  # 모집 인원

    # 모집 기간
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # 혜택 및 조건
    benefits = db.Column(db.Text, nullable=False)
    conditions = db.Column(db.Text, nullable=False)

    # 이미지
    image_url = db.Column(db.Text, nullable=True)

    # 상태 (RECRUITING, CLOSED, SELECTED)
    status = db.Column(db.String(20), nullable=False, default='RECRUITING')

    # 생성일 및 종료일
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    closed_at = db.Column(db.DateTime, nullable=True)

    # 관계
    advertiser = db.relationship('AdvertiserModel', back_populates='campaigns')
    applications = db.relationship('ApplicationModel', back_populates='campaign', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CampaignModel id={self.id} title={self.title} status={self.status}>'


# Advertiser 모델에 campaigns 관계 추가 필요
# (advertiser_model.py에서 추가)
