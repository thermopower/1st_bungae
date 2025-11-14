"""
Campaign Forms (WTForms)
체험단 생성 폼
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    DateField,
    FileField,
    SubmitField
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_wtf.file import FileAllowed
from datetime import date


class CampaignForm(FlaskForm):
    """체험단 생성 폼"""

    title = StringField(
        '체험단 제목',
        validators=[
            DataRequired(message='체험단 제목을 입력해주세요'),
            Length(min=5, max=100, message='제목은 5자 이상 100자 이하여야 합니다')
        ]
    )

    description = TextAreaField(
        '체험단 설명',
        validators=[
            DataRequired(message='체험단 설명을 입력해주세요'),
            Length(min=10, max=2000, message='설명은 10자 이상 2000자 이하여야 합니다')
        ]
    )

    quota = IntegerField(
        '모집 인원',
        validators=[
            DataRequired(message='모집 인원을 입력해주세요'),
            NumberRange(min=1, max=100, message='모집 인원은 1명 이상 100명 이하여야 합니다')
        ]
    )

    start_date = DateField(
        '모집 시작일',
        format='%Y-%m-%d',
        validators=[DataRequired(message='모집 시작일을 입력해주세요')]
    )

    end_date = DateField(
        '모집 종료일',
        format='%Y-%m-%d',
        validators=[DataRequired(message='모집 종료일을 입력해주세요')]
    )

    benefits = TextAreaField(
        '제공 혜택',
        validators=[
            DataRequired(message='제공 혜택을 입력해주세요'),
            Length(min=5, max=500, message='제공 혜택은 5자 이상 500자 이하여야 합니다')
        ]
    )

    conditions = TextAreaField(
        '체험 조건',
        validators=[
            DataRequired(message='체험 조건을 입력해주세요'),
            Length(min=5, max=500, message='체험 조건은 5자 이상 500자 이하여야 합니다')
        ]
    )

    image = FileField(
        '대표 이미지',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='이미지 파일만 업로드 가능합니다 (jpg, jpeg, png, gif)')
        ]
    )

    submit = SubmitField('체험단 생성')

    def validate(self, extra_validators=None):
        """커스텀 검증"""
        if not super().validate(extra_validators):
            return False

        # 날짜 검증: 시작일은 오늘 이후
        if self.start_date.data and self.start_date.data < date.today():
            self.start_date.errors.append('모집 시작일은 오늘 이후여야 합니다')
            return False

        # 날짜 검증: 종료일은 시작일 이후
        if (self.start_date.data and self.end_date.data and
                self.end_date.data <= self.start_date.data):
            self.end_date.errors.append('모집 종료일은 시작일 이후여야 합니다')
            return False

        return True


class CampaignApplicationForm(FlaskForm):
    """체험단 지원 폼"""

    application_reason = TextAreaField(
        '지원 사유',
        validators=[
            Optional(),
            Length(max=1000, message='지원 사유는 1000자 이하여야 합니다')
        ],
        render_kw={
            "placeholder": "지원 사유를 입력해주세요 (선택사항)",
            "rows": 5
        }
    )

    submit = SubmitField('지원하기')
