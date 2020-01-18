####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, request, Blueprint
from flask_login import current_user

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog.models import BlogPost
from blog import db

####################################################
# BLUEPRINT SETUP ##################################
####################################################

core = Blueprint('core', __name__)

####################################################
# INDEX SETUP ######################################
####################################################

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    try:
        query1 = BlogPost.query.order_by(BlogPost.views.desc()).filter(BlogPost.category!=current_user.last_viewed_catagory)
        query2 = BlogPost.query.order_by(BlogPost.views.desc()).filter_by(category=current_user.last_viewed_catagory)
        blog_posts = BlogPost.query.order_by(BlogPost.views.desc())
        blog_posts.filter(BlogPost.category==current_user.last_viewed_catagory).filter(BlogPost.category!=current_user.last_viewed_catagory)
    except:
        blog_posts = BlogPost.query.order_by(BlogPost.views.desc())
    
    blog_posts = blog_posts.paginate(page=page, per_page=5)
    return render_template('index.html', page_name="Home", blog_posts=blog_posts)

####################################################
# ABOUT SETUP ######################################
####################################################

@core.route('/about')
def about():
    return render_template('about.html')