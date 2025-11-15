"""
Supabase 기존 테이블 삭제 스크립트
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("Supabase 기존 테이블 삭제 중...")

    # 테이블 삭제 (외래 키 제약 조건 때문에 순서 중요)
    tables_to_drop = [
        'application',
        'campaign',
        'influencer',
        'advertiser',
        'users',
        'alembic_version'  # 마이그레이션 버전 테이블도 삭제
    ]

    for table_name in tables_to_drop:
        try:
            db.session.execute(db.text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))
            print(f"  [OK] {table_name} deleted")
        except Exception as e:
            print(f"  [FAIL] {table_name} failed: {e}")

    db.session.commit()
    print("\n모든 테이블이 삭제되었습니다!")
