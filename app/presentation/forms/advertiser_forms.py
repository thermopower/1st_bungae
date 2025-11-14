"""Advertiser Forms (WTForms)"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
import re
from datetime import date, datetime


class AdvertiserRegistrationForm(FlaskForm):
    """광고주 정보 등록 폼"""

    # 공통 정보
    name = StringField(
        '이름',
        validators=[
            DataRequired(message='이름을 입력해주세요'),
            Length(min=2, max=100, message='이름은 2자 이상 100자 이하여야 합니다')
        ],
        render_kw={"placeholder": "홍길동", "class": "form-control"}
    )

    birth_date = DateField(
        '생년월일',
        validators=[DataRequired(message='생년월일을 입력해주세요')],
        format='%Y-%m-%d',
        render_kw={"class": "form-control", "type": "date"}
    )

    phone_number = StringField(
        '휴대폰번호',
        validators=[
            DataRequired(message='휴대폰번호를 입력해주세요'),
            Regexp(r'^010-\d{4}-\d{4}$', message='올바른 휴대폰번호 형식을 입력해주세요 (010-XXXX-XXXX)')
        ],
        render_kw={"placeholder": "010-1234-5678", "class": "form-control", "id": "phoneNumber"}
    )

    # 광고주 전용 정보
    business_name = StringField(
        '업체명',
        validators=[
            DataRequired(message='업체명을 입력해주세요'),
            Length(min=2, max=100, message='업체명은 2자 이상 100자 이하여야 합니다')
        ],
        render_kw={"placeholder": "테스트 카페", "class": "form-control"}
    )

    address = StringField(
        '주소',
        validators=[DataRequired(message='주소를 입력해주세요')],
        render_kw={"placeholder": "서울시 강남구 테헤란로 123", "class": "form-control", "id": "address"}
    )

    business_phone = StringField(
        '업장 전화번호',
        validators=[
            DataRequired(message='업장 전화번호를 입력해주세요'),
            Regexp(r'^\d{2,3}-\d{3,4}-\d{4}$', message='올바른 전화번호 형식을 입력해주세요 (예: 02-1234-5678)')
        ],
        render_kw={"placeholder": "02-1234-5678", "class": "form-control"}
    )

    business_number = StringField(
        '사업자등록번호',
        validators=[
            DataRequired(message='사업자등록번호를 입력해주세요'),
            Regexp(r'^\d{3}-\d{2}-\d{5}$', message='사업자등록번호는 XXX-XX-XXXXX 형식이어야 합니다')
        ],
        render_kw={"placeholder": "123-45-67890", "class": "form-control", "id": "businessNumber"}
    )

    representative_name = StringField(
        '대표자명',
        validators=[
            DataRequired(message='대표자명을 입력해주세요'),
            Length(min=2, max=100, message='대표자명은 2자 이상 100자 이하여야 합니다')
        ],
        render_kw={"placeholder": "김대표", "class": "form-control"}
    )

    submit = SubmitField('등록', render_kw={"class": "btn btn-primary"})

    def validate_birth_date(self, field):
        """생년월일 검증: 만 19세 이상"""
        if field.data:
            today = date.today()
            age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
            if age < 19:
                raise ValidationError('만 19세 이상만 가입 가능합니다.')
