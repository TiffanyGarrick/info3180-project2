from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, ValidationError, PasswordField,TextAreaField
from wtforms.validators import DataRequired, Email


def my_length_check(form, field):
    if len(field.data) > 30:
        raise ValidationError('Field must be less than 30 characters')
    
class MyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), my_length_check])
    password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired(), my_length_check])
    lastname = StringField('Last Name', validators=[DataRequired(), my_length_check]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class PhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])
    description = StringField('Description', validators=[DataRequired()])