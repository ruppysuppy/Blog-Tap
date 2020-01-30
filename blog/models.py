####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db, login_manager

####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta
from random import randint

####################################################
# USER LOADER SETUP ################################
####################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

####################################################
# USER MODEL SETUP #################################
####################################################

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, nullable=False)
    last_viewed_catagory1 = db.Column(db.String(64), index=True)
    last_viewed_catagory2 = db.Column(db.String(64), index=True)
    last_viewed_catagory3 = db.Column(db.String(64), index=True)

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.confirmed = False
        self.profile_image = "profile_img_" + str(randint(1, 9)) + ".png"
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User-name: {self.username}\nEmail: {self.email}"

####################################################
# BLOG POST MODEL SETUP ############################
####################################################

class BlogPost(db.Model):
    __tablename__ = 'BlogPost'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(64), nullable=False)

    def __init__(self, user_id, title, text, category):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.category = category
        self.views = 0
    
    def __repr__(self):
        return f"Post ID: {self.id} -- {self.date}\nTitle: {self.title.upper()}"

####################################################
# FOLLOWERS MODEL SETUP ############################
####################################################

class Followers(db.Model):
    __tablename__ = 'Followers'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id
    
    def __repr__(self):
        return f"Follower ID: {self.follower_id}\tFollowed ID: {self.followed_id}"

####################################################
# NOTIFICATION MODEL SETUP #########################
####################################################

class Notifications(db.Model):
    __tablename__ = 'Notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.String(150), nullable=False)
    link_id = db.Column(db.Integer, nullable=False)
    is_blog = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_id, text, link_id, is_blog):
        self.user_id = user_id
        self.text = text
        self.link_id = link_id
        self.is_blog = is_blog
    
    def __repr__(self):
        return f"User ID: {self.userer_id}\tTime: {self.date}\nText: {self.text}"
    
    @classmethod
    def delete_expired(cls):
        expiration_days = 14
        limit = datetime.now() - timedelta(days=expiration_days)
        cls.query.filter(cls.date <= limit).delete()
        db.session.commit()

####################################################
# VIEW MODEL SETUP #################################
####################################################

class View(db.Model):
    __tablename__ = 'View'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('BlogPost.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, blog_id):
        self.user_id = user_id
        self.blog_id = blog_id
    
    def __repr__(self):
        return f"User ID: {self.userer_id}\tBlog ID: {self.blog_id}"

    @classmethod
    def delete_expired(cls):
        expiration_days = 2
        limit = datetime.now() - timedelta(days=expiration_days)
        cls.query.filter(cls.timestamp <= limit).delete()
        db.session.commit()
