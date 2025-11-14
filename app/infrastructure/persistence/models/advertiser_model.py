"""Advertiser SQLAlchemy Model"""

from app.extensions import db
from datetime import datetime


class AdvertiserModel(db.Model):
    """
    광고주 ORM 모델

    Attributes:
        id: 광고주 ID (자동 증가)
        user_id: User 테이블 참조 (UUID)
        name: 이름
        birth_date: 생년월일
        phone_number: 휴대폰번호
        business_name: 업체명
        address: 주소
        business_phone: 업장 전화번호
        business_number: 사업자등록번호
        representative_name: 대표자명
        created_at: 등록일
    """

    __tablename__ = "advertiser"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    business_phone = db.Column(db.String(20), nullable=False)
    business_number = db.Column(db.String(10), unique=True, nullable=False)
    representative_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # 관계
    user = db.relationship("UserModel", back_populates="advertiser")
    campaigns = db.relationship("CampaignModel", back_populates="advertiser", cascade="all, delete")

    def __repr__(self):
        return f"<AdvertiserModel(id={self.id}, user_id='{self.user_id}', business_name='{self.business_name}')>"
