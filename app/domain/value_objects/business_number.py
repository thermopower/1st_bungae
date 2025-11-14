"""BusinessNumber Value Object"""

import re
from app.domain.exceptions import InvalidBusinessNumberException


class BusinessNumber:
    """
    사업자등록번호 값 객체 (불변)

    10자리 숫자
    """

    def __init__(self, value: str):
        """
        BusinessNumber 초기화

        Args:
            value: 사업자등록번호 (하이픈 있거나 없거나)

        Raises:
            InvalidBusinessNumberException: 사업자등록번호 형식이 잘못된 경우
        """
        if not value or not isinstance(value, str):
            raise InvalidBusinessNumberException(value if value else "")

        # 하이픈 제거
        clean_value = value.replace("-", "")

        if not re.match(r"^\d{10}$", clean_value):
            raise InvalidBusinessNumberException(value)

        self._value = clean_value

    @property
    def value(self) -> str:
        """사업자등록번호 값 (읽기 전용)"""
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, BusinessNumber):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"BusinessNumber('{self._value}')"
