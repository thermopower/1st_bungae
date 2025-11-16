"""
Storage Provider Interface
Infrastructure Layer - External Services Interface
"""
from abc import ABC, abstractmethod
from typing import Optional


class IStorageProvider(ABC):
    """스토리지 제공자 인터페이스"""

    @abstractmethod
    def upload_file(self, bucket: str, path: str, file_data: bytes) -> str:
        """
        파일 업로드

        Args:
            bucket: 버킷 이름
            path: 파일 경로
            file_data: 파일 데이터

        Returns:
            str: 업로드된 파일의 URL
        """
        pass

    @abstractmethod
    def delete_file(self, bucket: str, path: str) -> bool:
        """
        파일 삭제

        Args:
            bucket: 버킷 이름
            path: 파일 경로

        Returns:
            bool: 삭제 성공 여부
        """
        pass

    @abstractmethod
    def get_file_url(self, bucket: str, path: str) -> Optional[str]:
        """
        파일 URL 조회

        Args:
            bucket: 버킷 이름
            path: 파일 경로

        Returns:
            Optional[str]: 파일 URL
        """
        pass
