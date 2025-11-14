"""Email Value Object 테스트 (TDD)"""

import pytest


class TestEmail:
    """Email Value Object 테스트"""

    def test_email_valid(self):
        """정상 케이스: 유효한 이메일"""
        from app.domain.value_objects.email import Email

        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_email_minimum_length(self):
        """경계 케이스: 최소 길이 이메일"""
        from app.domain.value_objects.email import Email

        email = Email("a@b.c")
        assert email.value == "a@b.c"

    def test_email_invalid_format(self):
        """에러 케이스: 잘못된 형식"""
        from app.domain.value_objects.email import Email
        from app.domain.exceptions import InvalidEmailException

        with pytest.raises(InvalidEmailException, match="Invalid email format"):
            Email("invalid-email")

    def test_email_empty_string(self):
        """에러 케이스: 빈 문자열"""
        from app.domain.value_objects.email import Email
        from app.domain.exceptions import InvalidEmailException

        with pytest.raises(InvalidEmailException):
            Email("")

    def test_email_equality(self):
        """동등성 테스트"""
        from app.domain.value_objects.email import Email

        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("other@example.com")

        assert email1 == email2
        assert email1 != email3

    def test_email_hash(self):
        """해시 테스트"""
        from app.domain.value_objects.email import Email

        email1 = Email("test@example.com")
        email2 = Email("test@example.com")

        assert hash(email1) == hash(email2)
