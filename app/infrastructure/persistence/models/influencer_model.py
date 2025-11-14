"""
Influencer ORM 모델
"""
from app import db
from datetime import datetime


class InfluencerModel(db.Model):
    """인플루언서 데이터베이스 모델"""

    __tablename__ = 'influencer'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    channel_name = db.Column(db.String(100), nullable=False)
    channel_url = db.Column(db.Text, nullable=False)
    follower_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('UserModel', back_populates='influencer')
    applications = db.relationship('ApplicationModel', back_populates='influencer', cascade='all, delete')

    def __repr__(self):
        return f'<InfluencerModel {self.id}: {self.name}>'
