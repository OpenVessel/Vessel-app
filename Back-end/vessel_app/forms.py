
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, AnyOf

from vessel_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=45)])
    password = PasswordField('Password', validators=[DataRequired()]) ## dont forgot change length of password to 10
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()
            
        if user:
            raise ValidationError('Username is taken chose another.')
            
    def validate_email(self, email):
        
        user = User.query.filter_by(email=email.data).first()
            
        if user:
            raise ValidationError('email is taken  chose another.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    recaptcha = RecaptchaField()

class SessionIDForm(FlaskForm):
    session_id = StringField('Session ID')
    submit = SubmitField('Process')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
                        
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            
            if user:
                raise ValidationError('Username is taken.')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            
            if user:
                raise ValidationError('Email is taken.')
    