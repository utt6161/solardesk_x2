import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Email, Regexp, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message="Поле обязательно к заполнению")])
    password = PasswordField('password')



class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message="Поле обязательно к заполнению"), Length(min=5, max=20)])
    password = PasswordField('password', validators=[DataRequired(message="Поле обязательно к заполнению"), Length(min=4, max=12)])
    email = EmailField('email', validators=[DataRequired(message="Поле обязательно к заполнению"), Email(message='Email не удовлетворяет требованиям. Пример: test@test.ru')])
    phone_number = TelField('phone_number', validators=[DataRequired(message="Поле обязательно к заполнению"),
                                                        Regexp(r'^((\+7|7|8)+([0-9]){10})$', re.IGNORECASE,
                                                               'Телефон может начинаться с +7, 7, 8 и иметь формат 9992223344')])
    first_name = StringField('first_name', validators=[DataRequired(message="Поле обязательно к заполнению")])
    middle_name = StringField('middle_name')
    last_name = StringField('last_name', validators=[DataRequired(message="Поле обязательно к заполнению")])
