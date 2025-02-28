from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .auth import User
import bcrypt

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    db = current_app.config['db']
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists
        if db.users.find_one({'username': username}):
            flash("Username already exists.")
            return redirect(url_for('main.register'))

        # Hash the password before storing it
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.users.insert_one({'username': username, 'password': hashed})

        flash("Registration successful. Please log in.")
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    db = current_app.config['db']
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_doc = db.users.find_one({'username': username})
        if user_doc and bcrypt.checkpw(password.encode('utf-8'), user_doc['password']):
            user = User(user_doc)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('main.protected'))
        flash("Invalid username or password.")
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.login'))


@main.route('/protected')
@login_required
def protected():
    return f"Hello, {current_user.username}! This page is protected."
