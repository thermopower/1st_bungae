"""Auth Forms (회원가입, 로그인 폼)"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo


class RegisterForm(FlaskForm):
    """회원가입 폼"""

    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요'),
        Email(message='올바른 이메일 형식을 입력해주세요')
    ])

    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요'),
        Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다'),
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)',
            message='비밀번호는 영문과 숫자를 포함해야 합니다'
        )
    ])

    password_confirm = PasswordField('비밀번호 확인', validators=[
        DataRequired(message='비밀번호 확인을 입력해주세요'),
        EqualTo('password', message='비밀번호가 일치하지 않습니다')
    ])

    submit = SubmitField('회원가입')


class LoginForm(FlaskForm):
    """로그인 폼"""

    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요'),
        Email(message='올바른 이메일 형식을 입력해주세요')
    ])

    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요')
    ])

    submit = SubmitField('로그인')
