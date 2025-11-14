"""PhoneNumber Value Object"""

import re
from app.domain.exceptions import InvalidPhoneNumberException


class PhoneNumber:
    """
    전화번호 값 객체 (불변)

    010으로 시작하는 11자리 숫자 (하이픈 자동 추가)
    """

    PHONE_REGEX = r"^010\d{8}$"

    def __init__(self, value: str):
        """
        PhoneNumber 초기화

        Args:
            value: 전화번호 (하이픈 있거나 없거나)

        Raises:
            InvalidPhoneNumberException: 전화번호 형식이 잘못된 경우
        """
        if not value or not isinstance(value, str):
            raise InvalidPhoneNumberException(value if value else "")

        # 하이픈 제거
        clean_value = value.replace("-", "")

        if not re.match(self.PHONE_REGEX, clean_value):
            raise InvalidPhoneNumberException(value)

        # 하이픈 추가 포맷팅: 010-1234-5678
        formatted = f"{clean_value[:3]}-{clean_value[3:7]}-{clean_value[7:]}"
        self._value = formatted

    @property
    def value(self) -> str:
        """전화번호 값 (읽기 전용)"""
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, PhoneNumber):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"PhoneNumber('{self._value}')"
