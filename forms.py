from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo

# Next three items (two functions and a class) are for the form validation
# Existing validator for the 'name' field
def validate_name(form, field):
    if "RobertHiene" in field.data:
        raise ValidationError("Your message has been rejected. Please Stop.")

def validate_subject(form, field):
    blocked_words = ["write", "writing", "wrote"]
    if any(word in field.data.lower() for word in blocked_words):
        raise ValidationError("Your message has been marked as spam. If this is a mistake, please email us directly at boonewh@pathsixdesigns.com")
        
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please enter your name."), validate_name])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address"), Email()])
    subject = StringField("What is your current website? (ex: www.name.com or 'none' is also fine.)", validators=[DataRequired(message="Please enter a site or none."), validate_subject])
    message = TextAreaField("Briefly describe what you need in your new website. 'Not sure' is a valid response.", validators=[DataRequired(message="Please enter a message. I don't know or I want to talk about it are good responses.")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")

#Below here the CRM forms are defined. They will be split out when we transition to a package w/blueprints.

class RegistrationFrom(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class LoginFrom(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
