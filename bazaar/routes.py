# Python file exclusively for specifying routes
from flask.helpers import flash
from bazaar import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from bazaar.models import Item, User
from bazaar.forms import RegisterForm, LoginForm
from bazaar import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/bazaar')
# pulling information from database bazaar.db
def bazaar_page():
    items = Item.query.all()
    return render_template('bazaar.html', items=items)

# Important to add both GET and POST methods, otherwise Method won't be accepted
# Error here – possible that the method for storing passwords with HASH does not work
@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
# Conditional for creating a new user, will be similarly used for login
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data, 
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('bazaar_page'))
    # Checking for errors in the form
    if form.errors != {}: #This wants to say if there are no errors in the validation
        for err_msg in form.errors.values():
            flash(f'There was an error when creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

# It is more difficult to validate an existing user due to the hash password storing
# To overcome this, I am using code from BCrypt library
# Refer to models.py
# Once user successfully logs in, a flash message pops up
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Logged in successfully as: {attempted_user.username}', category='success')
            return redirect(url_for('bazaar_page'))
        else:
            flash('Incorrect username and/or password.', category='danger')

    return render_template('login.html', form=form)
