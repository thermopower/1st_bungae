"""DateTimeUtils 테스트"""

import pytest
from datetime import date


class TestParseDate:
    """parse_date 함수 테스트"""

    def test_parse_date_valid(self):
        """정상 케이스: 유효한 날짜"""
        from app.shared.utils.datetime_utils import parse_date

        result = parse_date("2025-11-14")
        assert result == date(2025, 11, 14)

    def test_parse_date_invalid_format(self):
        """에러 케이스: 잘못된 형식"""
        from app.shared.utils.datetime_utils import parse_date
        from app.domain.exceptions import ValidationException

        with pytest.raises(ValidationException, match="Invalid date format"):
            parse_date("2025/11/14")


class TestDaysBetween:
    """days_between 함수 테스트"""

    def test_days_between(self):
        """정상 케이스: 날짜 차이 계산"""
        from app.shared.utils.datetime_utils import days_between

        date1 = date(2025, 11, 14)
        date2 = date(2025, 11, 20)
        assert days_between(date1, date2) == 6
