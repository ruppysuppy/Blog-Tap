####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db
from blog.models import User, BlogPost
from blog.users.forms import Register, UpdateUserForm, LoginForm

####################################################
# BLUEPRINT SETUP ##################################
####################################################

users = Blueprint('user', __name__)

####################################################
# REGISTRATION SETUP ###############################
####################################################

@users.route('/register', methods=["GET", "POST"])
def register():
    form = Register()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if (user == None):
            user = User(email=form.email.data, username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            flash(f'Thankyou for registering at Blog Tap. Welcome {form.username.data}!')

            return redirect(url_for('user.login'))
        
        else:
            flash('Email already registered')
            return redirect(url_for('user.regiser'))
    
    return render_template('register.html', form=form, page_name="Registration")

####################################################
# LOGIN SETUP ######################################
####################################################

@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if (user is not None and user.check_password(form.password.data)):
            login_user(user)
            flash('Login Successful!')

            next = request.args.get('next')

            if (next == None or not next[0] == '/'):
                next = url_for('core.index')
            
            return redirect(next)
        
        else:
            flash('Incorrect Username/Password!')
            return redirect(url_for('user.login'))
    
    return render_template('login.html', form=form, page_name="Login")

####################################################
# LOGOUT SETUP #####################################
####################################################

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

####################################################
# ACCOUNT UPDATION SETUP ###########################
####################################################

@users.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        current_user.username = form.username.data

        flash('Username Updated!')

        db.session.commit()

        return redirect(url_for('user.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
    
    profile_image = url_for('static', filename='img/'+current_user.profile_image)

    return render_template('account.html', profile_image=profile_image, form=form)

####################################################
# LIST BLOGS (USER SPECIFIC) #######################
####################################################

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.views.desc()).paginate(page=page, per_page=5)

    return render_template('user_blog_posts.html', user=user, blog_posts=blog_posts)
