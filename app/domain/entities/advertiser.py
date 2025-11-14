"""Advertiser Entity (광고주 도메인 엔티티)"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Advertiser:
    """
    광고주 도메인 엔티티

    Attributes:
        id (Optional[int]): 광고주 ID (자동 증가)
        user_id (str): User 테이블 참조 (UUID)
        name (str): 이름
        birth_date (date): 생년월일
        phone_number (str): 휴대폰번호 (010-XXXX-XXXX)
        business_name (str): 업체명
        address (str): 주소
        business_phone (str): 업장 전화번호
        business_number (str): 사업자등록번호 (10자리)
        representative_name (str): 대표자명
        created_at (datetime): 등록일
    """

    id: Optional[int]
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    business_name: str
    address: str
    business_phone: str
    business_number: str
    representative_name: str
    created_at: datetime

    def __eq__(self, other) -> bool:
        """동등성: ID가 같으면 동일한 광고주"""
        if not isinstance(other, Advertiser):
            return False
        # ID가 None이 아니고 같으면 동일
        if self.id is not None and other.id is not None:
            return self.id == other.id
        # ID가 None이면 user_id로 비교
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        """해시: ID 기반 (ID가 None이면 user_id 기반)"""
        if self.id is not None:
            return hash(self.id)
        return hash(self.user_id)
