# This file defines CLI commands registered via Flask's built-in Click integration.
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime
import click
from flask.cli import with_appcontext
from flask_security import hash_password

from app import db
from app.models.user_models import User, Role


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo('Database initialized.')


def init_db():
    """Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """Create users"""

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    find_or_create_user(u'Admin Example', u'admin@example.com', 'Password1', admin_role)
    find_or_create_user(u'Member Example', u'member@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """Find existing role or create new role"""
    role = db.session.execute(db.select(Role).filter_by(name=name)).scalar_one_or_none()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(full_name, email, password, role=None):
    """Find existing user or create new user"""
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    if not user:
        user = User(email=email,
                    full_name=full_name,
                    password=hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.now(datetime.timezone.utc))
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
