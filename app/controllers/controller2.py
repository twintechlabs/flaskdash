# Copyright 2020 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm
import uuid, json, os
import datetime

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
controller2_blueprint = Blueprint('controller2', __name__, template_folder='templates')

@controller2_blueprint.route('/example', methods=['GET'])
def sample_page():

    return render_template('views/controller2/example.html')


