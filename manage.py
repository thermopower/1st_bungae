"""
데이터베이스 마이그레이션 관리 스크립트
"""
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from flask_migrate import Migrate, init, migrate as migrate_cmd, upgrade
from app import create_app
from app.extensions import db

# Flask 앱 생성
app = create_app()

# Flask-Migrate 초기화
migration = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        if len(sys.argv) > 1:
            command = sys.argv[1]

            if command == 'init':
                print("마이그레이션 폴더 초기화 중...")
                init()
                print("완료!")

            elif command == 'migrate':
                message = sys.argv[2] if len(sys.argv) > 2 else "Auto migration"
                print(f"마이그레이션 파일 생성 중: {message}")
                migrate_cmd(message=message)
                print("완료!")

            elif command == 'upgrade':
                print("데이터베이스에 마이그레이션 적용 중...")
                upgrade()
                print("완료!")

            else:
                print("사용법:")
                print("  python manage.py init      - 마이그레이션 초기화")
                print("  python manage.py migrate   - 마이그레이션 파일 생성")
                print("  python manage.py upgrade   - 데이터베이스에 적용")
        else:
            print("사용법:")
            print("  python manage.py init      - 마이그레이션 초기화")
            print("  python manage.py migrate   - 마이그레이션 파일 생성")
            print("  python manage.py upgrade   - 데이터베이스에 적용")
