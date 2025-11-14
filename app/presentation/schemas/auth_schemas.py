"""Auth Schemas (DTOs)"""

from dataclasses import dataclass


@dataclass
class RegisterRequestDTO:
    """회원가입 요청 DTO"""
    email: str
    password: str


@dataclass
class RegisterResponseDTO:
    """회원가입 응답 DTO"""
    user_id: str
    email: str
