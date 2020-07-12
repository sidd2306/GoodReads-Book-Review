from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user,login_required,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(usrn=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Wrong credentials, Please try again!')

    login_user(user)
    return redirect(url_for('main.home'))


@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(usrn=username).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.register_post'))

    new_user = User(name=name, usrn=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    flash('Account created successfully')
    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
