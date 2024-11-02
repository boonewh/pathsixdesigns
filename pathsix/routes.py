from flask import render_template, request, redirect, url_for, flash
from pathsix import app, mail, bcrypt, db
from pathsix.forms import ContactForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask_mail import Message
from pathsix.models import User, Client, Address, ContactNote, Sale, BillingCycle, WebsiteUpdate, MailingList, ClientWebsite, Reminder
from flask_login import login_user, current_user, logout_user, login_required

# Sample data for the customers page
companies = [
    {
        'company': 'Acme, Inc.',
        'address': '130 Main St.',
        'city': 'Boston',
        'state': 'MA',
        'zipcode': '02108',
        'email': 'doe@acme.com',
        'phone': '555-555-5555'
    },
    {
        'company': 'Widgets, LLC',
        'address': '123 Main St.',
        'city': 'Boston',
        'state': 'MA',
        'zipcode': '02108',
        'email': 'jane@widgets.com',
        'phone': '555-555-5556'
    },
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            for field_errors in form.errors.values():
                for error in field_errors:
                    flash(error, 'error')
            return redirect(url_for('contact'))
        else:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']]
            )
            msg.body = f"""
            This message was sent from the PathSix Web Design contact form.

            From: {form.name.data} <{form.email.data}>
            Message:
            {form.message.data}
            """
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/crm')
def crm():
    return render_template('crm/crm.html') 

@app.route('/customers')
@login_required
def customers():
    return render_template('crm/customers.html', companies=companies)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('crm'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('crm/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('crm'))   
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('crm/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('crm'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('crm/account.html', form=form)