from flask import render_template, redirect, flash, url_for, request
from blogapp import app, db
from blogapp.models import User, Post
from blogapp.forms import RegistrationForm, LoginForm
from blogapp import bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
            flash('Login Unsuccessful. Please check your email and password you have entered', 'red')
    return render_template('auth/login.html',title = "Login", form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit() :
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email= form.email.data, password = hased_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'green')
        return redirect(url_for('login'))
    return render_template('auth/register.html',title = "Register", form = form)

@app.route('/logout', methods=['POST', 'GET'])
def logout ():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def  account():
    return render_template('accounts.html', title = 'Accounts')