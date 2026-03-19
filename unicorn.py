"""This file starts the application using gunicorn for production use.

Usage:
    gunicorn --bind 0.0.0.0:5000 "app:create_app()"
"""

from app import create_app

app = create_app()
