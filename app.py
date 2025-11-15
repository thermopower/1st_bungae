"""
Flask 애플리케이션 진입점
"""
import os
from flask import Flask
from dotenv import load_dotenv
from app.config import Config
from app.extensions import db, login_manager, cors
from app.routes import auth, main, advertiser, influencer

# 환경변수 로드
load_dotenv()


def create_app(config_class=Config):
    """Flask 애플리케이션 팩토리"""
    app = Flask(__name__,
                template_folder='app/templates',
                static_folder='app/static')
    app.config.from_object(config_class)

    # 확장 초기화
    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    # 블루프린트 등록
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(advertiser.bp)
    app.register_blueprint(influencer.bp)

    # 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()

    return app


# Render/Gunicorn을 위한 애플리케이션 인스턴스
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
