from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_migrate import current

from app.forms import signupForm, signinForm, updateUsernameForm

from app.models import db, User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix='/auth')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = signinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            print('This user is ready to be checked if they gave the right username and password')
            print(form.username.data, form.password.data)
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not check_password_hash(user.password, form.password.data):

                flash('Username or password did not match. Try again.', category='danger')
                return redirect(url_for('auth.signin'))

            login_user(user)
            print(current_user, current_user.__dict__)
            flash(f'Thanks for logging in, {user.username}.', category='info')
            return redirect(url_for('home'))
        else:

            flash('Bad form input, try again', category='warning')
            return redirect(url_for('auth.signin'))

    return render_template('signin.html', form=form) 

@auth.route('/register', methods=['GET', 'POST'])
def signup():

    form = signupForm()

    if request.method == 'POST': 

        if form.validate_on_submit():
            print('successful new user data received')
            new_user = User(form.username.data, form.email.data, form.password.data, form.first_name.data, form.last_name.data)        
            print(f'New user created - {new_user.__dict__}')
           
            try:
                db.session.add(new_user)
                db.session.commit()
            except:
                flash('Username or email already taken - please try again.', category='warning')
                return redirect(url_for('auth.signup'))
            login_user(new_user)
            flash(f'Thanks for signing up, {new_user.first_name} {new_user.last_name}!', category='info')
            return redirect(url_for('home'))
        else:

            flash('Bad form input, try again', category='warning')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html', form=form) 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.signin'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = updateUsernameForm() 

    if request.method == 'POST':

        if form.validate_on_submit() and check_password_hash(current_user.password, form.password.data):
           
            if User.query.filter_by(username=form.newusername.data).first():
                flash('Username already taken. Please try a different one.', category='danger')
                return redirect(url_for('auth.profile'))
            else:
               
                current_user.username = form.newusername.data 
                db.session.commit() 
                flash('Your username has been updated!', category='success')
                return redirect(url_for('auth.profile'))
        else:
            flash('Incorrect password- try again.', category='danger')
            return redirect(url_for('auth.profile'))

    return render_template('profile.html', form=form)