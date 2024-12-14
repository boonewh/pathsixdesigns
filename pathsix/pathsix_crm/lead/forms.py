from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional, URL, Length, Regexp

class LeadsForm(FlaskForm):
    # Lead Information
    name = StringField(
        'Company Name',
        validators=[
            DataRequired(message="Company name is required."),
            Length(max=100, message="Company name cannot exceed 100 characters.")
        ]
    )
    website = StringField(
        'Current Website',
        validators=[
            Optional(),
            URL(message="Please provide a valid URL."),
            Length(max=255, message="Website URL cannot exceed 255 characters.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            Optional(),
            Email(message="Please provide a valid email address."),
            Length(max=120, message="Email cannot exceed 120 characters.")
        ]
    )
    phone = StringField(
        'Phone',
        validators=[
            Optional(),
            Length(max=20, message="Phone number cannot exceed 20 characters."),
            Regexp(r'^\+?[0-9\s-]+$', message="Please provide a valid phone number.")
        ]
    )

    # Contact Person Information
    first_name = StringField(
        'Contact First Name',
        validators=[
            Optional(),
            Length(max=50, message="First name cannot exceed 50 characters.")
        ]
    )
    last_name = StringField(
        'Contact Last Name',
        validators=[
            Optional(),
            Length(max=50, message="Last name cannot exceed 50 characters.")
        ]
    )
    contact_email = StringField(
        'Contact Email',
        validators=[
            Optional(),
            Email(message="Please provide a valid contact email."),
            Length(max=120, message="Contact email cannot exceed 120 characters.")
        ]
    )
    contact_phone = StringField(
        'Contact Phone',
        validators=[
            Optional(),
            Length(max=20, message="Contact phone cannot exceed 20 characters."),
            Regexp(r'^\+?[0-9\s-]+$', message="Please provide a valid phone number.")
        ]
    )

    # Address Information
    street = StringField(
        'Street',
        validators=[
            Optional(),
            Length(max=255, message="Street address cannot exceed 255 characters.")
        ]
    )
    city = StringField(
        'City',
        validators=[
            Optional(),
            Length(max=100, message="City cannot exceed 100 characters.")
        ]
    )
    state = StringField(
        'State',
        validators=[
            Optional(),
            Length(max=2, message="State must be 2 characters."),
            Regexp(r'^[A-Z]{2}$', message="State must be a valid 2-letter code (e.g., TX).")
        ]
    )
    zip_code = StringField(
        'Zip Code',
        validators=[
            Optional(),
            Length(max=10, message="Zip Code cannot exceed 10 characters."),
            Regexp(r'^\d{5}(?:-\d{4})?$', message="Please provide a valid zip code (e.g., 12345 or 12345-6789).")
        ]
    )

    # Contact Note
    contact_note = TextAreaField(
        'Note',
        validators=[
            Optional(),
            Length(max=500, message="Note cannot exceed 500 characters.")
        ]
    )

    # Submit Button
    submit = SubmitField('Add Lead')
