####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

####################################################
# SEARCH FORM SETUP ################################
####################################################

class Search_Form(FlaskForm):
    param = StringField('Search for User/Blog', validators=[DataRequired()])
    submit = SubmitField('Search')