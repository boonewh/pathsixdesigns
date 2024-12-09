from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Project Description', validators=[Optional(), Length(max=1000)])
    status = SelectField(
        'Status',
        choices=[('won', 'Won'), ('lost', 'Lost'), ('In Progress', 'In Progress'), ('on hold', 'On Hold'), ('canceled', 'Canceled')],
        validators=[DataRequired()]
    )
    start = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    worth = FloatField('Project Worth ($)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Create Project')
