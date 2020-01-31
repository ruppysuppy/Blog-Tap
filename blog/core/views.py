####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, request, Blueprint
from flask_login import current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog.core.search_engine import search
from blog.models import BlogPost, Notifications, View
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
    View.delete_expired()
    Notifications.delete_expired()
    
    page = request.args.get('page', 1, type=int)

    blog_posts = BlogPost.query.order_by(BlogPost.views.desc(), BlogPost.date.desc()).paginate(page=page, per_page=6)
    if (current_user.is_authenticated):
        ids = db.engine.execute(f'select blog_id        \
                                  from View             \
                                  where user_id={current_user.id}')
        viewed = [id_blog[0] for id_blog in ids]
        categories = [current_user.last_viewed_catagory1, current_user.last_viewed_catagory2, current_user.last_viewed_catagory3]
        recommended = BlogPost.query.filter(BlogPost.category.in_(categories), BlogPost.author!=current_user, ~(BlogPost.id.in_(viewed))).order_by(BlogPost.views.desc(), BlogPost.date.desc()).paginate(page=page, per_page=3, error_out=False)
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
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []
    
    return render_template('about.html', notifs=notifs)

####################################################
# SEARCH SETUP #####################################
####################################################

@core.route('/search/<string:param>')
@login_required
def search_page(param):
    users, blogs = search(param)
    
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []
    
    return render_template('search.html', notifs=notifs, param=param, users=users, blogs=blogs)