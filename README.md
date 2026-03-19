# FlaskDash starter app v2.0

![Screenshot](https://github.com/twintechlabs/flaskdash/blob/master/app/static/images/screenshot.png)

This code base serves as a starting point for writing your next Flask application.

It's based on the awesome work of Ling Thio and includes the open source
CoreUI admin Bootstrap theme and a number of enhancements to the base Flask
starter app including basic user management and a separate view file for
API code.

## Code characteristics

* Tested on Python 3.13
* Well organized directories with lots of comments
    * app
        * commands
        * controllers
        * models
        * static
        * templates
    * tests
* Includes test framework (`pytest` and `tox`)
* Includes database migration framework (`Flask-Migrate` / `alembic`)
* Sends error emails to admins for unhandled exceptions


## Setting up a development environment

We assume that you have `git` and Python 3.13 installed.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/twintechlabs/flaskdash.git my_app

    # Create a virtual environment and activate it
    cd ~/dev/my_app
    python3.13 -m venv .venv
    source .venv/bin/activate

    # Install required Python packages
    pip install -r requirements.txt


## Configuring SMTP

Edit the `app/local_settings.py` file and set the `MAIL_...` settings to match
your SMTP provider.

You should also set a strong, unique value for `SECURITY_PASSWORD_SALT` in
`local_settings.py`. Do not use the default value in production.


## Initializing the Database

    # Create DB tables and populate the roles and users tables
    flask init-db


## Running the app (development)

    # Start the Flask development web server
    flask run

Point your web browser to http://localhost:5000/

You can make use of the following seed users:
- email `member@example.com` with password `Password1`
- email `admin@example.com` with password `Password1`


## Running the app (production)

Gunicorn is included in `requirements.txt`. To run in production:

    gunicorn --bind 0.0.0.0:5000 "app:create_app()"

Or use `unicorn.py` as the entry point:

    gunicorn unicorn:app


## Database migrations

When you change a model, generate and apply a migration:

    flask db migrate -m "Description of change"
    flask db upgrade

If you are upgrading an existing database from v1.x, you must run a migration
to add the `fs_uniquifier` column required by Flask-Security-Too:

    flask db migrate -m "Add fs_uniquifier to users"
    flask db upgrade


## Running the automated tests

    pytest tests/

    # With coverage:
    pytest tests/ --cov=app


## Using Server-side Sessions

FlaskDash has Flask-Session built in, configured to use the SQLAlchemy backend
by default. The sessions table is created automatically by `flask init-db`.

You can change the backend in `local_settings.py` by setting `SESSION_TYPE`
to `redis`, `filesystem`, or other supported backends.

Usage example:

    session['key'] = 'value'
    val = session.get('key', 'not set')


## Trouble shooting

If you make changes to models and run into DB schema issues during development,
delete the SQLite DB file `app.sqlite` and re-run `flask init-db`.


## Key dependencies

* [CoreUI](https://coreui.io/)
* [Flask](https://flask.palletsprojects.com/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Security-Too](https://flask-security-too.readthedocs.io/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-Session](https://flask-session.readthedocs.io/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/)


## Authors
- Matt Hogan - matt AT twintechlabs DOT io
- Ling Thio -- ling.thio AT gmail DOT com

<!-- Please consider leaving this line. Thank you -->
[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.
