from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

customers = [
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
            if "Your message has been rejected. Please Stop." in form.name.errors:
                flash("Your message has been rejected.")
            else:
                flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
            msg.body = """ 
            This message was sent from the PathSix Web Design contact form.

            From: %s <%s> 
            %s 
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', success=True)
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
    
@app.route('/crm')
def crm():
    return render_template('crm.html') 

@app.route('/customers_page')
def customers_page():
    return render_template('customers_page.html', customers=customers)
