from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from pathsix import db, bcrypt, limiter
from pathsix.models import User
from pathsix.pathsix_crm.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, UserForm
from pathsix.pathsix_crm.users.utils import send_reset_email
from flask import Blueprint
from flask_security import roles_required

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
@roles_required('admin') 
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'User added successfully, they may now log in.', 'success')
        
        # Clear the form so the admin can easily add another user
        return redirect(url_for('users.register'))  # Redirect to the same page to add more users
    
    return render_template('crm/user/register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Allows 5 login attempts per minute <------------------ Rate Limiting
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('crm_main.crm'))   
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('crm/user/login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('crm_main.crm'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('crm/user/account.html', form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
@limiter.limit("3 per minute")  # Allows 3 password reset attempts per minute <------------------ Rate Limiting
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('crm_main.crm'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('crm/user/reset_request.html', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('crm_main.crm'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('crm/user/reset_token.html', form=form)


# Admin routes: Could be moved to Admin Blueprint ideally.
@users.route('/users', methods=['GET'])
@roles_required('admin')
def users_page():
    users_list = User.query.all()  # Fetch all users from the database
    form = UserForm()  # Assuming you have a UserForm for creating users
    return render_template('crm/user/users_page.html', users_list=users_list, form=form)

@users.route('/users/add', methods=['POST'])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user added successfully!', 'success')
        return redirect(url_for('users.users_page'))
    flash('Failed to add user. Please check the form for errors.', 'danger')
    return redirect(url_for('users.users_page'))

@users.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users.users_page'))
