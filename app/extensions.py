"""
Flask 확장 초기화
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# SQLAlchemy 인스턴스
db = SQLAlchemy()

# Flask-Login 설정
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '로그인이 필요합니다.'

# CORS 설정
cors = CORS()
