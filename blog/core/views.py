####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, request, Blueprint
from flask_login import current_user

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog.models import BlogPost, Notifications
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

    blog_posts = BlogPost.query.order_by(BlogPost.views.desc()).paginate(page=page, per_page=10)
    if (current_user.is_authenticated):
        recommended = BlogPost.query.filter_by(category=current_user.last_viewed_catagory).filter(BlogPost.author != current_user).order_by(BlogPost.views.desc()).paginate(page=page, per_page=2, error_out=False)
    else:
        recommended = None
    
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('index.html', page_name="Home", blog_posts=blog_posts, recommended=recommended, notifs=notifs)

####################################################
# ABOUT SETUP ######################################
####################################################

@core.route('/about')
def about():
    return render_template('about.html')