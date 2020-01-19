####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

####################################################
# BLOG POST FORM SETUP #############################
####################################################

class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = event_selector = SelectField("Category", choices=[
        ('Education', 'Education'), 
        ('Finances', 'Finances'), 
        ('Fitness', 'Fitness'), 
        ('Food', 'Food'), 
        ('Gaming', 'Gaming'), 
        ('Health', 'Health'), 
        ('Lifestyle', 'Lifestyle'), 
        ('Movie', 'Movie'), 
        ('Music', 'Music'), 
        ('News', 'News'), 
        ('Parenting', 'Parenting'), 
        ('Personal', 'Personal'), 
        ('Politics', 'Politics'), 
        ('Religious', 'Religious'), 
        ('Self-Development', 'Self-Development'), 
        ('Sports', 'Sports'), 
        ('Technology', 'Technology'), 
        ('Travel', 'Travel')
    ])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Post")