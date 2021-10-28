from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            return jsonify(
                msg='Please check your login details and try again.',status=401,icon='error')
        
        login_user(user, remember=False)
        return jsonify(msg='Grant Access.',status=200, icon='success')
    if request.method == "GET":
        return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    password = request.form.get('password')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    rol_id = request.form.get('rol')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        # flash('Email address already exists')
        return jsonify(msg='Email address already exists.', status=409, icon='warning')
        # return redirect(url_for('auth.signup'))


    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, nombre=nombre, password=generate_password_hash(password, method='sha256'), direccion= direccion,telefono=telefono,rol_id= rol_id, estado='A')

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # return redirect(url_for('auth.login'))
    return jsonify(msg='Grabación exitosa.', status=200, icon='success')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))