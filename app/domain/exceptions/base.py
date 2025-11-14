"""
Domain Base Exception

모든 도메인 예외의 베이스 클래스
"""


class DomainException(Exception):
    """
    모든 도메인 예외의 베이스 클래스

    Attributes:
        message (str): 예외 메시지
        http_status_code (int): HTTP 상태 코드 (기본값: 500)
    """

    def __init__(self, message: str, http_status_code: int = 500):
        """
        DomainException 초기화

        Args:
            message: 예외 메시지
            http_status_code: HTTP 상태 코드 (기본값: 500)

        Raises:
            ValueError: 메시지가 비어있거나 None인 경우
        """
        if not message:
            raise ValueError("Error message cannot be empty")

        self.message = message
        self.http_status_code = http_status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """예외 문자열 표현"""
        return self.message

    def __repr__(self) -> str:
        """예외 repr 표현"""
        return f"{self.__class__.__name__}(message='{self.message}', http_status_code={self.http_status_code})"
