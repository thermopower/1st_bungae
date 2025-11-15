"""
Flask 애플리케이션 패키지 (Factory Pattern)
"""

from flask import Flask
from app.extensions import db, migrate, login_manager, cors, csrf
from app.config import Config


def create_app(config_class=Config):
    """
    Flask 애플리케이션 팩토리

    Args:
        config_class: 설정 클래스 (기본값: Config)

    Returns:
        Flask: 초기화된 Flask 앱
    """
    app = Flask(__name__,
                template_folder='presentation/templates',
                static_folder='static')
    app.config.from_object(config_class)

    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)

    # Blueprint 등록
    from app.presentation.routes.auth_routes import auth_bp
    from app.presentation.routes.main_routes import main_bp
    from app.presentation.routes.advertiser_routes import advertiser_bp
    from app.presentation.routes.influencer_routes import influencer_bp
    from app.presentation.routes.campaign_routes import campaign_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(advertiser_bp)
    app.register_blueprint(influencer_bp)
    app.register_blueprint(campaign_bp)

    # UserModel import (user_loader 등록을 위해)
    with app.app_context():
        from app.infrastructure.persistence.models import user_model

    return app
