"""
인플루언서 관련 DTO (Data Transfer Object)
"""
from dataclasses import dataclass
from datetime import date


@dataclass
class InfluencerRegistrationRequestDTO:
    """인플루언서 정보 등록 요청 DTO"""
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    channel_name: str
    channel_url: str
    follower_count: int


@dataclass
class InfluencerResponseDTO:
    """인플루언서 응답 DTO"""
    id: int
    user_id: str
    name: str
    channel_name: str
    channel_url: str
    follower_count: int
