"""
에러 핸들링 데코레이터
Shared Layer - Decorators
"""
from functools import wraps
from flask import jsonify, render_template
from app.domain.exceptions.base import DomainException


def handle_domain_exceptions(f):
    """
    도메인 예외를 HTTP 응답으로 변환하는 데코레이터

    Usage:
        @app.route('/some-route')
        @handle_domain_exceptions
        def some_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except DomainException as e:
            # 도메인 예외를 사용자 친화적 에러 메시지로 변환
            return render_template(
                'error.html',
                error_message=str(e),
                error_code=e.error_code if hasattr(e, 'error_code') else 400
            ), 400
        except Exception as e:
            # 예상치 못한 예외 처리
            return render_template(
                'error.html',
                error_message='시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
                error_code=500
            ), 500
    return decorated_function


def handle_api_exceptions(f):
    """
    API 엔드포인트용 예외를 JSON 응답으로 변환하는 데코레이터

    Usage:
        @app.route('/api/some-route')
        @handle_api_exceptions
        def some_api_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except DomainException as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'error_code': e.error_code if hasattr(e, 'error_code') else 400
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': '시스템 오류가 발생했습니다.',
                'error_code': 500
            }), 500
    return decorated_function
