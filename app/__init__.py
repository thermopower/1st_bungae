"""
Flask 애플리케이션 패키지 (Factory Pattern)
"""

from flask import Flask
from app.extensions import db
from app.config import Config


def create_app(config_class=Config):
    """
    Flask 애플리케이션 팩토리

    Args:
        config_class: 설정 클래스 (기본값: Config)

    Returns:
        Flask: 초기화된 Flask 앱
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 확장 초기화
    db.init_app(app)

    # Blueprint 등록
    from app.presentation.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
