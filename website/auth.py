from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash("Будь ласка, заповніть всі поля", "error")
            return redirect(url_for("auth.login"))
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('first_name')
        occupation = request.form.get('occupation')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif first_name is None:
            flash('First name is required.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')



        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
    email=email, 
    first_name=first_name, 
    last_name=last_name, 
    occupation=occupation,
    password=generate_password_hash(password1, method='pbkdf2:sha256')
)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("html_registr.html", user=current_user)

@auth.route("/profile")
@login_required
def profile():
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('my_profile.html', title='Profile', image_file=image_file)

@auth.route("/contacts")
@login_required
def contacts():
    return render_template('contacts.html', title='Contacts')

@auth.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    image_file = url_for('static', filename='images/' + current_user.image_file)
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.occupation = request.form.get('occupation')
        current_user.notes = request.form.get('notes')
        db.session.commit()
        flash('Ваші дані профілю були оновлені!', category='success')
        return redirect(url_for('auth.profile'))

    return render_template('edit.html', title='Edit profile', image_file=image_file)
