# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>, Matt Hogan <matt@twintechlabs.io>

import uuid
from flask_security import UserMixin, RoleMixin
from flask_security.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db


# Define the Role data model
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the User data model. Make sure to add the flask_security.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-Security)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    fs_uniquifier = db.Column(db.String(255), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))

    # User information
    full_name = db.Column(db.Unicode(100), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def has_role(self, role):
        for item in self.roles:
            if item.name == role:
                return True
        return False

    def role(self):
        for item in self.roles:
            return item.name

    def name(self):
        return str(self.full_name)


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Extended registration form that adds full_name to Flask-Security's built-in form
class ExtendedRegisterForm(RegisterForm):
    full_name = StringField('Full Name', validators=[validators.DataRequired('Full Name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[validators.DataRequired('Full Name is required')])
    submit = SubmitField('Save')
