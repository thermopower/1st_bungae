"""Main Routes (홈 페이지 등)"""

from flask import Blueprint, render_template

# Blueprint 생성
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """홈 페이지 (추후 구현)"""
    return "<h1>1st Bungae - 체험단 매칭 플랫폼</h1><p>홈 페이지입니다.</p>"
