from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

# Create a form class
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please enter your name.")])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address"), Email()])
    subject = StringField("What is your current website? (ex: www.name.com or \"none\" is also fine.)", validators=[DataRequired(message="Please enter a site or none.")])
    message = TextAreaField("Briefly describe what you need in your new website. \"Not sure\" is a valid reponse.", validators=[DataRequired(message="Please enter a message. I don't know or I want to talk about it are good responses.")])
    submit = SubmitField("Send")