"""ValidationUtils 테스트"""


class TestIsInRange:
    """is_in_range 함수 테스트"""

    def test_is_in_range(self):
        """정상 케이스: 범위 내"""
        from app.shared.utils.validation_utils import is_in_range

        assert is_in_range(5, min_value=1, max_value=10) is True

    def test_is_in_range_boundary(self):
        """경계 케이스: 경계 값"""
        from app.shared.utils.validation_utils import is_in_range

        assert is_in_range(1, min_value=1, max_value=10) is True
        assert is_in_range(10, min_value=1, max_value=10) is True

    def test_is_out_of_range(self):
        """에러 케이스: 범위 밖"""
        from app.shared.utils.validation_utils import is_in_range

        assert is_in_range(0, min_value=1, max_value=10) is False
        assert is_in_range(11, min_value=1, max_value=10) is False


class TestIsInList:
    """is_in_list 함수 테스트"""

    def test_is_in_list(self):
        """정상 케이스: 리스트에 포함"""
        from app.shared.utils.validation_utils import is_in_list

        assert is_in_list("apple", ["apple", "banana"]) is True

    def test_is_not_in_list(self):
        """에러 케이스: 리스트에 없음"""
        from app.shared.utils.validation_utils import is_in_list

        assert is_in_list("orange", ["apple", "banana"]) is False
