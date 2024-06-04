# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Pno',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    pno = StringField('Pno',
                         id='username_create',
                         validators=[DataRequired()])
    name = StringField('Name',
                         id='name_create',
                         validators=[DataRequired()])
    role = StringField('Role',
                      id='Role_create',
                      validators=[DataRequired()])
    type = StringField('Type',
                         id='type_create',
                         validators=[DataRequired()])
    status = StringField('Status',
                         id='Status', default="ACTIVE")
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    
