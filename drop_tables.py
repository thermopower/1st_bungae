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

    # 먼저 public 스키마의 모든 테이블 조회
    result = db.session.execute(db.text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """))

    all_tables = [row[0] for row in result]
    print(f"Found {len(all_tables)} tables to drop: {', '.join(all_tables)}\n")

    # 모든 테이블을 CASCADE로 삭제
    for table_name in all_tables:
        try:
            db.session.execute(db.text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))
            print(f"  [OK] {table_name} deleted")
        except Exception as e:
            print(f"  [FAIL] {table_name} failed: {e}")

    db.session.commit()
    print("\n모든 테이블이 삭제되었습니다!")
