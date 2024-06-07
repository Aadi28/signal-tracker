# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired

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
    
class NewSignalForm(FlaskForm):
    dtg = StringField('dtg',
                         id='dtg_create',
                         validators=[DataRequired()])
    from_origin = StringField('from_origin',
                         id='origin_create',
                         validators=[DataRequired()])
    to_destination = StringField('to_destination',
                         id='destination_create',
                         validators=[DataRequired()])
    info = StringField('info',
                         id='info_create')
    content = StringField('content',
                         id='content_create')
    priority = SelectField('priority',
                         id='priority_create',
                         choices=['OPS IMMEDIATE', 'PRIORITY', 'ROUTINE'],
                         validators=[DataRequired()])
    classification = SelectField('classification',
                         id='classification_create',
                         choices=['UNCLASS', 'RESTRICTED', 'CLASSIFIED', 'SECRET', 'TOP SECRET'],
                         validators=[DataRequired()])
    special_instructions = StringField('special_instructions',
                         id='spl_insstructions_create')