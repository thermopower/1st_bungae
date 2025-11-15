"""
Supabase 현재 테이블 목록 확인
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("Supabase current tables:")
    print("=" * 50)

    # 모든 테이블 조회
    result = db.session.execute(db.text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))

    tables = [row[0] for row in result]

    if tables:
        for table in tables:
            print(f"  - {table}")
    else:
        print("  No tables found")

    print("=" * 50)
    print(f"Total: {len(tables)} tables")
