

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