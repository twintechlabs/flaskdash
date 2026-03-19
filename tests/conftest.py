# This file contains pytest 'fixtures'.
# If a test functions specifies the name of a fixture function as a parameter,
# the fixture function is called and its result is passed to the test function.
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import pytest
from app import create_app, db as the_db

# Initialize the Flask-App with test-specific settings
the_app = create_app(dict(
    TESTING=True,                              # Propagate exceptions
    LOGIN_DISABLED=False,                      # Enable @login_required
    MAIL_SUPPRESS_SEND=True,                   # Disable Flask-Mail send
    SERVER_NAME='localhost',                   # Enable url_for() without request context
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
    WTF_CSRF_ENABLED=False,                    # Disable CSRF form validation
    SECURITY_PASSWORD_SALT='test-salt',        # Required by Flask-Security-Too
    SECURITY_WTF_CSRF_ENABLED=False,           # Disable CSRF for Flask-Security-Too forms
    SESSION_TYPE='filesystem',                 # Use filesystem sessions so flash messages survive redirects in tests
    SESSION_FILE_DIR='/tmp/flaskdash_test_sessions',
))

# Setup an application context (since the tests run outside of the webserver context)
the_app.app_context().push()

# Create and populate roles and users tables
from app.commands.init_db import init_db
init_db()


@pytest.fixture(scope='session')
def app():
    """ Makes the 'app' parameter available to test functions. """
    return the_app


@pytest.fixture(scope='session')
def db():
    """ Makes the 'db' parameter available to test functions. """
    return the_db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    db.session.begin_nested()
    yield db.session
    db.session.rollback()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
