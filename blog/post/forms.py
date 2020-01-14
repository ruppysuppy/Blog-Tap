####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

####################################################
# BLOG POST FORM SETUP #############################
####################################################

class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Post")