from flask import render_template, request, redirect, url_for, flash
from pathsix import app, mail
from pathsix.forms import ContactForm, RegistrationForm, LoginForm
from flask_mail import Message
from pathsix.models import Client, Address, ContactNote, Sale, BillingCycle, WebsiteUpdate, MailingList, ClientWebsite, Reminder

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
def customers():
    return render_template('crm/customers.html', companies=companies)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('crm'))
    return render_template('crm/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('crm'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('crm/login.html', form=form)
