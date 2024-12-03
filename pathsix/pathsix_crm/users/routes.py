from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_security import roles_required, hash_password
from pathsix import db
from pathsix.models import User, Role
from pathsix.pathsix_crm.users.forms import UpdateAccountForm, UserForm

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
    form = UserForm()  # Form for creating or managing users
    return render_template(
        'crm/user/users_page.html',
        users_list=users_list,
        form=form,
        available_roles=available_roles
    )


@users.route('/users/add', methods=['POST'])
@roles_required('admin')
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        # Check for existing email or username
        if User.query.filter_by(email=form.email.data).first():
            flash('A user with this email already exists.', 'danger')
            return redirect(url_for('users.users_page'))

        if User.query.filter_by(username=form.username.data).first():
            flash('A user with this username already exists.', 'danger')
            return redirect(url_for('users.users_page'))

        # Create new user
        hashed_password = hash_password(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)

        # Assign roles
        selected_role_name = form.role.data
        if selected_role_name:
            selected_role = Role.query.filter_by(name=selected_role_name).first()
            if selected_role:
                new_user.roles.append(selected_role)

        db.session.commit()
        flash('New user added successfully with the assigned role!', 'success')
    else:
        flash('Failed to add user. Please check the form for errors.', 'danger')

    return redirect(url_for('users.users_page'))


@users.route('/users/edit/<int:user_id>', methods=['POST'])
@roles_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    username = request.form.get('username')
    email = request.form.get('email')
    role_id = request.form.get('role')

    if not username or not email:
        flash('Username and email are required.', 'danger')
        return redirect(url_for('users.users_page'))

    try:
        user.username = username
        user.email = email

        # Update role
        if role_id:
            role = Role.query.get(role_id)
            if role:
                user.roles = [role]

        db.session.commit()
        flash('User updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user: {str(e)}', 'danger')

    return redirect(url_for('users.users_page'))


@users.route('/users/delete/<int:user_id>', methods=['POST'])
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users.users_page'))
