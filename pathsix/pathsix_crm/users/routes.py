from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from pathsix import db, bcrypt, limiter
from pathsix.models import User, Role
from pathsix.pathsix_crm.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, UserForm
from pathsix.pathsix_crm.users.utils import send_reset_email
from flask import Blueprint
from flask_security import roles_required, hash_password
from flask_mail import Message
from pathsix import mail  # Adjust the import based on your app structure

users = Blueprint('users', __name__)


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

@users.route('/users', methods=['GET'])
@roles_required('admin')
def users_page():
    users_list = User.query.all()  # Fetch all users
    available_roles = Role.query.all()  # Fetch all roles
    form = UserForm()  # Assuming you use a UserForm for creating users
    return render_template('crm/user/users_page.html', users_list=users_list, form=form, available_roles=available_roles)


@users.route('/users/add', methods=['POST'])
@roles_required('admin')
def add_user():
    form = UserForm()
    if not form.validate_on_submit():
        print("Form validation failed.")  # This should confirm failure
    else:
        print("Form validation succeeded, but it shouldn't!")  # Debugging


        # Check for existing email
        if User.query.filter_by(email=form.email.data).first():
            flash('A user with this email already exists.', 'danger')
            return redirect(url_for('users.users_page'))

        # Check for existing username
        if User.query.filter_by(username=form.username.data).first():
            flash('A user with this username already exists.', 'danger')
            return redirect(url_for('users.users_page'))

        # Create new user
        from flask_security.utils import hash_password

        hashed_password = hash_password(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)


        # Assign roles (assumes a 'role' field in the form)
        selected_role_name = form.role.data
        if selected_role_name:
            selected_role = Role.query.filter_by(name=selected_role_name).first()
            if selected_role:
                new_user.roles.append(selected_role)

        db.session.commit()

        print(f"Raw role data from form: {form.role.data}")
        flash('New user added successfully with the assigned role!', 'success')
        return redirect(url_for('users.users_page'))

    flash('Failed to add user. Please check the form for errors.', 'danger')
    return redirect(url_for('users.users_page'))

@users.route('/users/edit/<int:user_id>', methods=['POST'])
@roles_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    # Update user fields
    username = request.form.get('username')
    email = request.form.get('email')
    role_id = request.form.get('role')  # Fetch selected role ID

    if not username or not email:
        flash('Username and email are required.', 'danger')
        return redirect(url_for('users.users_page'))

    try:
        user.username = username
        user.email = email

        # Update role
        if role_id:
            role = Role.query.get(role_id)
            if role and role not in user.roles:
                user.roles = [role]

        db.session.commit()
        flash('User updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user: {str(e)}', 'danger')

    return redirect(url_for('users.users_page'))



@users.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users.users_page'))


# @users.route('/register', methods=['GET', 'POST'])
# @roles_required('admin') 
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'User added successfully, they may now log in.', 'success')
        
#         # Clear the form so the admin can easily add another user
#         return redirect(url_for('users.register'))  # Redirect to the same page to add more users
    
#     return render_template('crm/user/register.html', form=form)

# @users.route('/login', methods=['GET', 'POST'])
# @limiter.limit("5 per minute")  # Allows 5 login attempts per minute <------------------ Rate Limiting
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('crm_main.crm'))   
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'error')
#     return render_template('crm/user/login.html', form=form)


# @users.route('/reset_password', methods=['GET', 'POST'])
# @limiter.limit("3 per minute")  # Allows 3 password reset attempts per minute <------------------ Rate Limiting
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('crm_main.crm'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('crm/user/reset_request.html', form=form)

# @users.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('crm_main.crm'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('users.reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash(f'Your password has been updated! You can now log in.', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('crm/user/reset_token.html', form=form)

# @users.route('/users/add', methods=['POST'])
# @login_required
# def add_user():
#     form = UserForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('New user added successfully!', 'success')
#         return redirect(url_for('users.users_page'))
#     flash('Failed to add user. Please check the form for errors.', 'danger')
#     return redirect(url_for('users.users_page'))