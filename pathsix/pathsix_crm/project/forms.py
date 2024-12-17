from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Email

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_description = TextAreaField('Description', validators=[Optional()])
    project_status = SelectField('Status', choices=[('not started', 'Not Started'), ('in progress', 'In Progress'), ('completed', 'Completed')], validators=[DataRequired()])
    project_start = DateField('Start Date', validators=[Optional()])
    project_end = DateField('End Date', validators=[Optional()])
    project_worth = FloatField('Worth', validators=[Optional()])

    # Primary Project Contact fields
    contact_first_name = StringField('First Name', validators=[DataRequired()])
    contact_last_name = StringField('Last Name', validators=[DataRequired()])
    contact_email = StringField('Email', validators=[Optional(), Email()])
    contact_phone = StringField('Phone', validators=[Optional()])

    # Notes Field
    note = TextAreaField('Notes', validators=[Optional()])

# Submit button
    submit = SubmitField('Submit')  # Add this field