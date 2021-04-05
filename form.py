from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length,Email,EqualTo

class RegistrationForm(FlaskForm):
    napang=StringField('Nama Pangkalan',
    validators=[DataRequired(), Length(min=3, max=25)])
    email=StringField('Email', validators=[DataRequired()])
    submit=SubmitField('sign up')