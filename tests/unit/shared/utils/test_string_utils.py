"""StringUtils 테스트"""


class TestTruncate:
    """truncate 함수 테스트"""

    def test_truncate(self):
        """정상 케이스: 문자열 자르기"""
        from app.shared.utils.string_utils import truncate

        result = truncate("Hello World", max_length=5)
        assert result == "Hello..."

    def test_truncate_short_string(self):
        """경계 케이스: 짧은 문자열"""
        from app.shared.utils.string_utils import truncate

        result = truncate("Hi", max_length=10)
        assert result == "Hi"


class TestNormalizeWhitespace:
    """normalize_whitespace 함수 테스트"""

    def test_normalize_whitespace(self):
        """정상 케이스: 공백 정규화"""
        from app.shared.utils.string_utils import normalize_whitespace

        result = normalize_whitespace("  test  ")
        assert result == "test"
