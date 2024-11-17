from flask_wtf import FlaskForm, RecaptchaField
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo, URL, Optional
from pathsix.models import User

# Next three items (two functions and a class) are for the form validation
        
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please enter your name.")])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address"), Email()])
    subject = StringField("What is your current website? (ex: www.name.com or 'none' is also fine.)", validators=[DataRequired(message="Please enter a site or none.")])
    message = TextAreaField("Briefly describe what you need in your new website. 'Not sure' is a valid response.", validators=[DataRequired(message="Please enter a message. I don't know or I want to talk about it are good responses.")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")

    # Existing validator for the 'name' field
    def validate_name(self, field):
        if "RobertHiene" in field.data:
            raise ValidationError("Your message has been rejected. Please Stop.")

    def validate_subject(self, field):
        blocked_words = ["write", "writing", "wrote"]
        if any(word in field.data.lower() for word in blocked_words):
            raise ValidationError("Your message has been marked as spam. If this is a mistake, please email us directly at boonewh@pathsixdesigns.com")


#Below here the CRM forms are defined. They will be split out when we transition to a package w/blueprints.

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Taken. Please choose another.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("There is already an account using that email.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username Taken. Please choose another.")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("There is already an account using that email.")

class ClientForm(FlaskForm):
    # Client information
    name = StringField('Client Name', validators=[DataRequired(), Length(max=50)])
    website = StringField('Website', validators=[Optional(), URL(), Length(max=50)])
    pricing_tier = StringField('Pricing Tier', validators=[DataRequired(), Length(max=10)])
    email = StringField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])

    # Contact information
    first_name = StringField('Contact First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Contact Last Name', validators=[DataRequired(), Length(max=50)])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(max=20)])

    
    # Address information
    street = StringField('Street', validators=[DataRequired(), Length(max=255)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=2)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=10)])

    # Contact Note information
    contact_note = TextAreaField('Contact Note', validators=[Optional(), Length(max=500)])

    # Submit button
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")