from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm, RegistrationFrom, LoginFrom
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

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
            # Flash error messages for each field
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error, 'error')  # 'error' is the flash category for styling purposes
            return redirect(url_for('contact'))  # Redirect to display flash messages
        else:
            # Prepare and send the email
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
            return redirect(url_for('contact'))  # Redirect after success
    return render_template('contact.html', form=form)
    
@app.route('/crm')
def crm():
    return render_template('crm/crm.html') 

@app.route('/customers')
def customers():
    return render_template('crm/customers.html', companies=companies)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('crm'))
    return render_template('crm/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('crm'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('crm/login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)