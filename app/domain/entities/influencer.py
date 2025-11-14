"""
인플루언서 도메인 엔티티
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Influencer:
    """인플루언서 도메인 엔티티"""
    id: Optional[int]
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    channel_name: str
    channel_url: str
    follower_count: int
    created_at: datetime
