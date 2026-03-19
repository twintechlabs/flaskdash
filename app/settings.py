# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import os

# Application settings
APP_NAME = "Admin Flask Starter App"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Security settings
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = False         # Set True to require email confirmation
SECURITY_RECOVERABLE = True          # Allow password reset via email
SECURITY_CHANGEABLE = True           # Allow users to change their password
SECURITY_SEND_REGISTER_EMAIL = False # Set True to send confirmation emails
SECURITY_POST_LOGIN_VIEW = 'main.member_page'
SECURITY_POST_LOGOUT_VIEW = 'main.member_page'
SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
SECURITY_MSG_LOGGED_IN = ("You have signed in successfully", "success")
SECURITY_MSG_LOGGED_OUT = ("You have signed out successfully.", "info")
