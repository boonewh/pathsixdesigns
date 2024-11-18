from flask_mail import Message
from flask import url_for
import urllib.parse
from pathsix import mail


def send_reset_email(user):
    token = user.get_reset_token()
    encoded_token = urllib.parse.quote(token)  # URL-encode the token
    msg = Message('Password Reset Request', 
                  sender='noreply@pathsixdesigns.com', 
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg) 