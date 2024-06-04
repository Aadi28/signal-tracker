# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    pno = db.Column(db.String(255), primary_key=True)
    id = pno
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))
    status = db.Column(db.String(255))
    type = db.Column(db.String(255))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)

class Signal(db.Model):

    __tablename__ = 'signal_format'

    id = db.Column(db.String(255), primary_key=True)
    dtg = db.Column(db.String(255))
    from_origin = db.Column(db.String(255))
    to_destination = db.Column(db.String(255))
    info = db.Column(db.String(255))
    content = db.Column(db.String(255))
    priority = db.Column(db.String(255))
    classification = db.Column(db.String(255))
    tracking_id = db.Column(db.String(255))
    special_instructions = db.Column(db.String(255))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

class Signal_Tracking(db.Model):

    __tablename__ = 'signal_tracking'

    tracking_id = db.Column(db.String(255), primary_key=True)
    status = db.Column(db.String(255))
    signal_id = db.Column(db.String(255))
    held_with = db.Column(db.String(255))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.tracking_id)

@login_manager.user_loader
def user_loader(pno):
    return Users.query.filter_by(pno=pno).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('pno')
    user = Users.query.filter_by(pno=username).first()
    return user if user else None
