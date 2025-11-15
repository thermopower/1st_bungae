"""
인플루언서 관련 폼
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, URL, ValidationError
from datetime import date


class InfluencerRegistrationForm(FlaskForm):
    """인플루언서 정보 등록 폼"""

    # 공통 정보
    name = StringField('이름', validators=[
        DataRequired(message='이름을 입력해주세요'),
        Length(min=2, max=100, message='이름은 2자 이상 100자 이하여야 합니다')
    ])
    birth_date = DateField('생년월일', validators=[
        DataRequired(message='생년월일을 입력해주세요')
    ], format='%Y-%m-%d')
    phone_number = StringField('휴대폰번호', validators=[
        DataRequired(message='휴대폰번호를 입력해주세요'),
        Regexp(r'^010-\d{4}-\d{4}$', message='올바른 휴대폰번호 형식을 입력해주세요 (010-XXXX-XXXX)')
    ])

    # 인플루언서 전용 정보
    channel_type = SelectField('채널 유형', choices=[
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('blog', 'Blog'),
        ('other', '기타')
    ], default='youtube', validators=[DataRequired(message='채널 유형을 선택해주세요')])

    channel_name = StringField('SNS 채널명', validators=[
        DataRequired(message='SNS 채널명을 입력해주세요'),
        Length(min=2, max=100, message='채널명은 2자 이상 100자 이하여야 합니다')
    ])
    channel_url = StringField('채널 링크', validators=[
        DataRequired(message='채널 링크를 입력해주세요'),
        URL(message='올바른 URL 형식을 입력해주세요')
    ])
    follower_count = IntegerField('팔로워 수', validators=[
        DataRequired(message='팔로워 수를 입력해주세요'),
        NumberRange(min=0, message='팔로워 수는 0 이상이어야 합니다')
    ])

    submit = SubmitField('등록')

    def validate_birth_date(self, field):
        """생년월일 검증: 만 19세 이상"""
        if field.data:
            today = date.today()
            age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
            if age < 19:
                raise ValidationError('만 19세 이상만 가입 가능합니다.')
