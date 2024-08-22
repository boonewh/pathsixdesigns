from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

def validate_name(form, field):
    if "RobertHiene" in field.data:
        raise ValidationError("Your message has been rejected. Please Stop.")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please enter your name."), validate_name])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address"), Email()])
    subject = StringField("What is your current website? (ex: www.name.com or 'none' is also fine.)", validators=[DataRequired(message="Please enter a site or none.")])
    message = TextAreaField("Briefly describe what you need in your new website. 'Not sure' is a valid response.", validators=[DataRequired(message="Please enter a message. I don't know or I want to talk about it are good responses.")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")
