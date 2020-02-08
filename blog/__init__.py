####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_login import LoginManager
import os

####################################################
# APP SETUP ########################################
####################################################

app = Flask(__name__)

app.config["SECRET_KEY"] = 'secret_key'

####################################################
# DATABASE SETUP ###################################
####################################################

base_dir = os.path.abspath(os.path.dirname(__name__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

####################################################
# COOKIE SETUP #####################################
####################################################

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=28)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=28)

####################################################
# EMAIL SETUP ######################################
####################################################

app.config.update(
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = "youremailid(if its not from gmail, change the mail server)",
	MAIL_PASSWORD = "yourpassword"
	)

mail = Mail(app)

####################################################
# MIGRATION SETUP ##################################
####################################################

Migrate(app, db)

####################################################
# LOGIN SETUP ######################################
####################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

####################################################
# MISAKA SETUP (MARKDOWN CONVERTER) ################
####################################################

Misaka(app)

####################################################
# BLUEPRINT SETUP ##################################
####################################################

from blog.core.views import core
from blog.error_pages.handlers import error_pages
from blog.post.views import blog_posts
from blog.users.views import users

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(blog_posts)
app.register_blueprint(users)