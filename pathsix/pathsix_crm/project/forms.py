from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(max=255)])
    project_description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    project_status = SelectField(
        'Status',
        choices=[('in progress', 'In Progress'), ('completed', 'Completed')],
        validators=[DataRequired()]
    )
    project_start = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    project_end = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    project_worth = DecimalField('Worth', places=2, validators=[Optional()])
    submit = SubmitField('Save')
