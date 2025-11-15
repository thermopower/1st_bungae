"""
Flask 애플리케이션 진입점 (새로운 계층형 구조 사용)
"""
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# app/__init__.py의 create_app 사용
from app import create_app

# Flask 애플리케이션 생성
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
