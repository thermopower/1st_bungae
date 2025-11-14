"""Advertiser Schemas (DTO)"""

from dataclasses import dataclass
from datetime import date


@dataclass
class AdvertiserRegistrationRequestDTO:
    """광고주 정보 등록 요청 DTO"""
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    business_name: str
    address: str
    business_phone: str
    business_number: str
    representative_name: str


@dataclass
class AdvertiserResponseDTO:
    """광고주 정보 응답 DTO"""
    id: int
    user_id: str
    name: str
    business_name: str
    address: str
    business_phone: str
    representative_name: str
