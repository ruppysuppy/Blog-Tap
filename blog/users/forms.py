####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

# Imports for forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# Imports for users

from flask_login import current_user

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog.models import User

####################################################
# LOGIN FORM SETUP #################################
####################################################

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

####################################################
# REGISTER FORM SETUP ##############################
####################################################

class Register(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Both the Password Fields Must Match')])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email entered has already been registered')

####################################################
# UPDATE FORM SETUP ################################
####################################################

class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Update')
