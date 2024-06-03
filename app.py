from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():  # This replaces 'if request.method == 'POST':'
        try:
            msg = Message(form.subject.data, sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
            This message was sent from the PathSix Web Design contact form.

            From: {form.name.data} <{form.email.data}>
            {form.message.data}
            """
            mail.send(msg)
            return render_template('contact.html', success=True)
        except Exception as e:
            flash('An error occurred while sending the message. Please try again later.')
            return render_template('contact.html', form=form)
    else:
        # This else block now captures both GET requests and failed POST validations.
        if request.method == 'POST':
            flash('All fields are required.')  # You might want to keep or remove this line depending on your preference
        return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)