# app/infrastructure/persistence/models/application_model.py
"""
Application ORM Model (데이터베이스 테이블)
"""

from app.extensions import db
from datetime import datetime, UTC


class ApplicationModel(db.Model):
    """
    체험단 지원 ORM 모델 (application 테이블)

    인플루언서의 체험단 지원 정보 저장
    """

    __tablename__ = 'application'

    # 기본키
    id = db.Column(db.Integer, primary_key=True)

    # 외래키
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)

    # 지원 정보
    application_reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='APPLIED')  # APPLIED, SELECTED, REJECTED
    applied_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    # 중복 지원 방지
    __table_args__ = (
        db.UniqueConstraint('campaign_id', 'influencer_id', name='uq_application_campaign_influencer'),
    )

    # 관계
    campaign = db.relationship('CampaignModel', back_populates='applications')
    influencer = db.relationship('InfluencerModel', back_populates='applications')

    def __repr__(self):
        return f'<ApplicationModel id={self.id} campaign_id={self.campaign_id} influencer_id={self.influencer_id} status={self.status}>'
