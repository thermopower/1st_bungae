"""Email Value Object"""

import re
from app.domain.exceptions import InvalidEmailException


class Email:
    """
    이메일 값 객체 (불변)

    Attributes:
        value (str): 이메일 주소
    """

    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"

    def __init__(self, value: str):
        """
        Email 초기화

        Args:
            value: 이메일 주소

        Raises:
            InvalidEmailException: 이메일 형식이 잘못된 경우
        """
        if not value or not isinstance(value, str):
            raise InvalidEmailException(value if value else "")

        if not re.match(self.EMAIL_REGEX, value):
            raise InvalidEmailException(value)

        self._value = value

    @property
    def value(self) -> str:
        """이메일 값 (읽기 전용)"""
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Email):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Email('{self._value}')"
