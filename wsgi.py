"""
Flask 애플리케이션 진입점 (새로운 계층형 구조 사용)
"""
import os
import sys
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 프로덕션 환경에서 필수 환경변수 확인
required_env_vars = ['DATABASE_URL', 'SUPABASE_URL', 'SUPABASE_KEY', 'SECRET_KEY']
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]

if missing_vars and os.environ.get('FLASK_ENV') == 'production':
    print(f"❌ 필수 환경변수가 설정되지 않았습니다: {', '.join(missing_vars)}", file=sys.stderr)
    print("Render Dashboard > Environment 탭에서 환경변수를 설정해주세요.", file=sys.stderr)
    sys.exit(1)

# app/__init__.py의 create_app 사용
try:
    from app import create_app

    # Flask 애플리케이션 생성
    app = create_app()

    print("✅ Flask 애플리케이션이 성공적으로 시작되었습니다.")

except Exception as e:
    print(f"❌ Flask 애플리케이션 시작 실패: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    app.run(debug=True)
