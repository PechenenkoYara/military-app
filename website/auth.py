from flask import Blueprint, render_template, request, flash, redirect, url_for
from .data_checking import is_name_valid, is_valid_email, is_password_incorrect, is_valid_phone_number
from .contact_filter import filter_input
from .models import User, Contacts
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

import os
import secrets
from PIL import Image
from flask import current_app



auth = Blueprint('auth', __name__)



UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn




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
        elif not is_valid_email(email):
            flash("The email inputed is incorrect", category='error')
        elif not is_name_valid(first_name):
            flash("The first name inputed is incorrect", category='error')
        elif not is_name_valid(last_name):
            flash("The last name inputed is incorrect", category='error')
        elif is_password_incorrect(password1):
            flash(is_password_incorrect(password1), category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            new_user = User(email=email, \
                            first_name=first_name, \
                            last_name=last_name, \
                            occupation=occupation,\
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
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




@auth.route("/contacts", methods=['GET', 'POST'])
@login_required
def contacts():
    user_contacts = Contacts.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        occupation = request.form.get('occupation')

        if not is_valid_phone_number(number):
            flash("The phone number is incorrect", category='error')

        new_contact = Contacts(
            name=name,
            number=number,
            occupation=occupation,
            user_id=current_user.id
        )

        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('auth.contacts'))
    return render_template('contacts.html', title='Contacts', contacts=user_contacts)




@auth.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    image_file = url_for('static', filename='images/' + current_user.image_file)
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        current_user.occupation = request.form.get('occupation')
        current_user.notes = request.form.get('notes')

        if first_name and is_name_valid(first_name):
            current_user.first_name = first_name
        if last_name and is_name_valid(last_name):
            current_user.last_name = last_name

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '' and allowed_file(file.filename):
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(file.filename)
                picture_fn = random_hex + f_ext

                picture_path = os.path.join(current_app.root_path, 'static', 'images', picture_fn)

                output_size = (250, 250)
                i = Image.open(file)
                i.thumbnail(output_size)
                i.save(picture_path)

                if current_user.image_file != 'profile.png':
                    old_pic_path = os.path.join(current_app.root_path, 'static', 'images', current_user.image_file)
                    if os.path.exists(old_pic_path):
                        os.remove(old_pic_path)

                current_user.image_file = picture_fn

        old_p = request.form.get("old_password")
        new_p = request.form.get("new_password")
        check_p = request.form.get("check_password")

        if old_p or new_p or check_p:
            if not (old_p and new_p and check_p):
                flash("Please fill all password fields", "error")
                return redirect(url_for('auth.edit'))

            if is_password_incorrect(new_p):
                flash(is_password_incorrect(new_p), "error")
                return redirect(url_for('auth.edit'))

            if not check_password_hash(current_user.password, old_p):
                flash("Current password is incorrect", "error")
                return redirect(url_for('auth.edit'))

            if new_p != check_p:
                flash("New passwords don't match", "error")
                return redirect(url_for('auth.edit'))

            current_user.password = generate_password_hash(new_p)

        db.session.commit()
        flash('Профіль успішно оновлено!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('edit.html', title='Edit profile', image_file=image_file)
