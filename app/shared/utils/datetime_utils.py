"""DateTime Utils"""

from datetime import datetime, date
from app.domain.exceptions import ValidationException


def parse_date(date_string: str) -> date:
    """
    날짜 문자열을 date 객체로 변환

    Args:
        date_string: YYYY-MM-DD 형식의 날짜 문자열

    Returns:
        date 객체

    Raises:
        ValidationException: 형식이 잘못된 경우
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationException(f"Invalid date format, expected YYYY-MM-DD: {date_string}")


def days_between(date1: date, date2: date) -> int:
    """
    두 날짜 간의 일수 차이 계산

    Args:
        date1: 첫 번째 날짜
        date2: 두 번째 날짜

    Returns:
        일수 차이 (절대값)
    """
    return abs((date2 - date1).days)
