"""SocialChannel Value Object"""

from urllib.parse import urlparse
from app.domain.exceptions import ValidationException


class SocialChannel:
    """
    소셜 채널 값 객체 (불변)

    채널명과 URL을 포함
    """

    def __init__(self, channel_name: str, url: str):
        """
        SocialChannel 초기화

        Args:
            channel_name: 채널명
            url: 채널 URL

        Raises:
            ValidationException: 채널명이 비어있거나 URL이 잘못된 경우
        """
        if not channel_name or not isinstance(channel_name, str) or not channel_name.strip():
            raise ValidationException("Channel name cannot be empty")

        if not url or not isinstance(url, str):
            raise ValidationException(f"Invalid URL format: {url}")

        # URL 검증
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationException(f"Invalid URL format: {url}")

        self._channel_name = channel_name.strip()
        self._url = url

    @property
    def channel_name(self) -> str:
        """채널명 (읽기 전용)"""
        return self._channel_name

    @property
    def url(self) -> str:
        """URL (읽기 전용)"""
        return self._url

    def __eq__(self, other) -> bool:
        if not isinstance(other, SocialChannel):
            return False
        return self._channel_name == other._channel_name and self._url == other._url

    def __hash__(self) -> int:
        return hash((self._channel_name, self._url))

    def __str__(self) -> str:
        return f"{self._channel_name}: {self._url}"

    def __repr__(self) -> str:
        return f"SocialChannel(channel_name='{self._channel_name}', url='{self._url}')"
