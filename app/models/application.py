"""
체험단 지원 모델
"""
from app.extensions import db
from datetime import datetime


class Application(db.Model):
    """체험단 지원 정보"""

    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)

    # 지원 상태
    status = db.Column(db.String(20), default='pending')  # pending, selected, rejected
    message = db.Column(db.Text)  # 지원 메시지

    # 타임스탬프
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 복합 유니크 제약 (한 인플루언서는 한 캠페인에 한 번만 지원 가능)
    __table_args__ = (
        db.UniqueConstraint('campaign_id', 'influencer_id', name='unique_campaign_influencer'),
    )

    def __repr__(self):
        return f'<Application campaign_id={self.campaign_id} influencer_id={self.influencer_id}>'
