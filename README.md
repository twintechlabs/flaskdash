# FlaskDash starter app v1.3

![Screenshot](https://github.com/twintechlabs/flaskdash/blob/master/app/static/images/screenshot.png)

This code base serves as starting point for writing your next Flask application.

It's based on the awesome work of the Ling Thio and includes the open source
CoreUI admin BootStrap theme and a number of enhancements to the base Flask
Starter app including adding basic user management and a separate view file for
API code.

## Code characteristics

* Tested on Python 2.6, 2.7, 3.3, 3.4, 3.5, 3.6, and 3.7
* Well organized directories with lots of comments
    * app
        * commands
        * controllers
        * models
        * static
        * templates
    * tests
* Includes test framework (`py.test` and `tox`)
* Includes database migration framework (`alembic`)
* Sends error emails to admins for unhandled exceptions


## Setting up a development environment

We assume that you have `git` and `virtualenv` and `virtualenvwrapper` installed.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/twintechlabs/flaskdash.git my_app

    # Create the 'my_app' virtual environment
    mkvirtualenv -p PATH/TO/PYTHON my_app

    # Install required Python packages
    cd ~/dev/my_app
    workon my_app
    pip install -r requirements.txt


# Configuring SMTP

Edit the `local_settings.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html


## Initializing the Database

    # Create DB tables and populate the roles and users tables
    python manage.py init_db

    # Or if you have Fabric installed:
    fab init_db


## Running the app (development)

    # Start the Flask development web server
    python manage.py runserver

    # Or if you have Fabric installed:
    fab runserver

Point your web browser to http://localhost:5000/

You can make use of the following users:
- email `member@example.com` with password `Password1`.
- email `admin@example.com` with password `Password1`.

## Running the app (production)

To run the application in production mode, gunicorn3 is used (and included in requirements.txt.

    # Run the application in production mode
    ./runserver.sh

## Running the automated tests

    # Start the Flask development web server
    py.test tests/

    # Or if you have Fabric installed:
    fab test


## Using Server-side Sessions

Don't use server side session data! You should do everything you can to keep each request/response stateless. It'll be easier to maintain your code and easier to debug when something goes wrong.  

However, if you really need sessions, FlaskDash has Flask-Session built in (https://pythonhosted.org/Flask-Session/).  It is configured to use to the SQLAlchmey interface by default and the init_db command will set up a sessions table in your database.  You can change your configuration to use redis or MongoDB, as well.

Sessions are available in misc_views.py and can be added to any additional controllers you create.

This is how you might use it:

    # Session example
    session['key'] = 'value'
    val = session.get('key', 'not set')
    print(val)
    value    
    val = session.get('key2', 'not set')
    print(val)
    not set

## Trouble shooting

If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.


## Acknowledgements

With thanks to the following Flask extensions:
* [CoreUI](https://coreui.io/)
* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)
* [Flask-Session](https://pythonhosted.org/Flask-Session/)

<!-- Please consider leaving this line. Thank you -->
[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.

## Authors
- Matt Hogan - matt AT twintechlabs DOT io
- Ling Thio -- ling.thio AT gmail DOT com
