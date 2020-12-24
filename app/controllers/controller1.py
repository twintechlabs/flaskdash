# Copyright 2017 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template, current_app, session
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted
from flask_session import Session

from app import db
from app.models.user_models import UserProfileForm, User, UsersRoles, Role
import uuid, json, os
import datetime

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/')
def member_page():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    return render_template('views/controller1/member_base.html')

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('views/admin/users.html')

@main_blueprint.route('/users')
@roles_accepted('admin')
def user_admin_page():
    users = User.query.all()
    return render_template('views/admin/users.html',
        users=users)

@main_blueprint.route('/create_or_edit_user', methods=['GET', 'POST'])
@roles_accepted('admin')
def create_or_edit_user_page():
    form = UserProfileForm(request.form, obj=current_user)
    roles = Role.query.all()
    user_id = request.args.get('user_id')
    user = User()

    if user_id:
        user = User.query.filter(User.id == user_id).first()

    if request.method == 'POST':
        if user.id is None:
            user = User.query.filter(User.email == request.form['email']).first()
            if not user:
                user = User(email=request.form['email'],
                            full_name=request.form['full_name'],
                            password=current_app.user_manager.hash_password(request.form['password']),
                            active=True,
                            email_confirmed_at=datetime.datetime.utcnow())
                db.session.add(user)
                db.session.commit()
            return redirect(url_for('main.user_admin_page'))
        else:
            user.email = request.form['email']
            user.full_name = request.form['full_name']
            if request.form['password'] is not None and request.form['password'] is not "":
                user.password = current_app.user_manager.hash_password(request.form['password'])    
            db.session.commit()        
    return render_template('views/admin/edit_user.html',
                           form=form,
                           roles=roles,
                           user=user)

@main_blueprint.route('/manage_user_roles', methods=['GET', 'POST'])
@roles_accepted('admin')
def manage_user_roles():
    user_id = request.args.get('user_id')
    role_id = request.args.get('role_id')

    if user_id and role_id:
        user_id = int(user_id)
        role_id = int(role_id)
        db.session.query(UsersRoles).filter_by(user_id = user_id).filter_by(role_id = role_id).delete()
        db.session.commit()
    # Initialize form
    user_roles = list()
    if user_id is not None:
        user_id = int (user_id)
        user = User.query.filter_by(id=user_id).first()
        user_roles = user.roles

    form = UserProfileForm(request.form, obj=user)
    
    roles = db.session.query(Role).all()
    if request.method == 'POST':

        form.populate_obj(user) 
        if str(request.form['role']): 
            role = Role.query.filter(Role.name == str(request.form['role'])).first()
            user.roles.append(role)   
            db.session.commit()           
            flash('You successfully added a role to user '  + user.name() + ' !', 'success')  
        else:
            #user.roles = []  
            # print(f' Not appending role ') 
            flash('You failed to add a role to user '  + user.name() + ' !', 'failure')
            pass               
        
    return render_template('views/admin/manage_user_roles.html',
                            user=user,
                            roles=roles,
                            user_roles=user_roles,
                            form=form)

@main_blueprint.route('/delete_user', methods=['GET'])
@roles_accepted('admin')
def delete_user_page():
    try:
        user_id = request.args.get('user_id')

        db.session.query(UsersRoles).filter_by(user_id = user_id).delete()
        db.session.query(User).filter_by(id = user_id).delete()
        db.session.commit()

        flash('You successfully deleted your user!', 'success')
        return redirect(url_for('main.user_admin_page'))
    except Exception as e:
        flash('Opps!  Something unexpected happened.  On the brightside, we logged the error and will absolutely look at it and work to correct it, ASAP.', 'error')
        return redirect(request.referrer)

@main_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_profile_page'))

    # Process GET or invalid POST
    return render_template('views/controller1/user_profile_page.html',
                           current_user=current_user,
                           form=form)
