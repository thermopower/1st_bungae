"""
Supabase 클라이언트 유틸리티
"""
import os
from supabase import create_client, Client
from flask import current_app


def get_supabase_client() -> Client:
    """Supabase 클라이언트 인스턴스 반환"""
    url = current_app.config.get('SUPABASE_URL')
    key = current_app.config.get('SUPABASE_KEY')

    if not url or not key:
        raise ValueError('SUPABASE_URL과 SUPABASE_KEY가 설정되어야 합니다.')

    return create_client(url, key)


def get_supabase_admin_client() -> Client:
    """Supabase 관리자 클라이언트 인스턴스 반환"""
    url = current_app.config.get('SUPABASE_URL')
    key = current_app.config.get('SUPABASE_SERVICE_KEY')

    if not url or not key:
        raise ValueError('SUPABASE_URL과 SUPABASE_SERVICE_KEY가 설정되어야 합니다.')

    return create_client(url, key)
