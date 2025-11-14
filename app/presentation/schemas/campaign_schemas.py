# app/presentation/schemas/campaign_schemas.py
"""
Campaign DTO (Data Transfer Object)
Presentation Layer와 Application Layer 간 데이터 전달
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CampaignListItemDTO:
    """체험단 목록 아이템 DTO"""
    id: int
    title: str
    description_short: str  # 100자 이하
    image_url: Optional[str]
    quota: int
    application_count: int
    deadline: date
    business_name: str
    status: str


@dataclass
class CampaignDetailDTO:
    """체험단 상세 DTO"""
    id: int
    title: str
    description: str
    image_url: Optional[str]
    quota: int
    application_count: int
    start_date: date
    end_date: date
    benefits: str
    conditions: str
    status: str
    business_name: str
    business_address: str
    can_apply: bool  # 인플루언서가 지원 가능한지 여부
    already_applied: bool  # 이미 지원했는지 여부
