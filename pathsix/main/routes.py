from flask import render_template, request, redirect, url_for, flash
from pathsix import mail
from pathsix.main.forms import ContactForm
from flask_mail import Message
from flask import Blueprint, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pricing')
def pricing():
    return render_template('pricing.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            for field_errors in form.errors.values():
                for error in field_errors:
                    flash(error, 'error')
            return redirect(url_for('main.contact'))
        else:
            msg = Message(
                subject=form.subject.data,
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[current_app.config['MAIL_USERNAME']]
            )
            msg.body = f"""
            This message was sent from the PathSix Web Design contact form.

            From: {form.name.data} <{form.email.data}>
            Message:
            {form.message.data}
            """
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)
