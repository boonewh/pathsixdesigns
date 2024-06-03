from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_mail import Mail, Message
from config import EMAIL_PASSWORD, EMAIL_ADDRESS

app = Flask(__name__)
app.secret_key = 'pathsix033170'

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = EMAIL_ADDRESS
app.config["MAIL_PASSWORD"] = EMAIL_PASSWORD
mail.init_app(app)

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
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender=EMAIL_ADDRESS, recipients=[EMAIL_ADDRESS])
      msg.body = """ 
        This message was sent from the PathSix Web Design contact form.

        From: %s <%s> 
        %s 
        """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
  elif request.method == 'GET':
    return render_template('contact.html', form=form)