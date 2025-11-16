"""
Supabase Storage Provider Implementation
Infrastructure Layer - External Services
"""
from typing import Optional
from app.infrastructure.external.interfaces.i_storage_provider import IStorageProvider


class SupabaseStorageProvider(IStorageProvider):
    """Supabase Storage 구현체"""

    def __init__(self, client):
        """
        Supabase Storage 초기화

        Args:
            client: Supabase Client 인스턴스
        """
        self.client = client

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
        try:
            response = self.client.storage.from_(bucket).upload(path, file_data)

            # 공개 URL 반환
            return self.client.storage.from_(bucket).get_public_url(path)
        except Exception as e:
            raise Exception(f"파일 업로드 실패: {str(e)}")

    def delete_file(self, bucket: str, path: str) -> bool:
        """
        파일 삭제

        Args:
            bucket: 버킷 이름
            path: 파일 경로

        Returns:
            bool: 삭제 성공 여부
        """
        try:
            self.client.storage.from_(bucket).remove([path])
            return True
        except Exception as e:
            raise Exception(f"파일 삭제 실패: {str(e)}")

    def get_file_url(self, bucket: str, path: str) -> Optional[str]:
        """
        파일 URL 조회

        Args:
            bucket: 버킷 이름
            path: 파일 경로

        Returns:
            Optional[str]: 파일 URL
        """
        try:
            return self.client.storage.from_(bucket).get_public_url(path)
        except Exception:
            return None
