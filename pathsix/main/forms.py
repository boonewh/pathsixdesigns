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