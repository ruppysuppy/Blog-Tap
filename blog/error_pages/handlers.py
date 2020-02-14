####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import Blueprint, render_template
from flask_login import current_user

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog.models import Notifications

####################################################
# BLUEPRINT SETUP ##################################
####################################################

error_pages = Blueprint('error_pages', __name__)

####################################################
# ERROR 404 SETUP ##################################
####################################################

@error_pages.app_errorhandler(404)
def error_404(error):
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []
    return render_template('error_pages/404.html', notifs=notifs), 404

####################################################
# ERROR 403 SETUP ##################################
####################################################

@error_pages.app_errorhandler(403)
def error_403(error):
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []
    return render_template('error_pages/403.html', notifs=notifs), 403

####################################################
# ERROR 500 SETUP ##################################
####################################################

@error_pages.app_errorhandler(500)
def error_500(error):
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []
    return render_template('error_pages/500.html', notifs=notifs),500