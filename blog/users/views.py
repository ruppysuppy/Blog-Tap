####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, logout_user, current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db
from blog.models import User, BlogPost, Notifications, Followers
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
            return redirect(url_for('user.register'))
    
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
            session.permanent = True

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
    flash('Successfully logged out!')
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

        flash('The Changes have been saved!')

        db.session.commit()

        return redirect(url_for('user.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
    
    elif request.method == "POST":
        pic_num = request.form["profile-img"]
        current_user.profile_image = current_user.profile_image[:-5] + pic_num + '.png'
        db.session.commit()

        form.username.data = current_user.username
    
    profile_image = url_for('static', filename='img/'+current_user.profile_image)

    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('account.html', profile_image=profile_image, form=form, notifs=notifs)

####################################################
# LIST BLOGS (USER SPECIFIC) #######################
####################################################

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.views.desc(), BlogPost.date.desc()).paginate(page=page, per_page=6)

    get_following = Followers.query.filter(Followers.follower_id==current_user.id, Followers.followed_id==user.id).first()
    if (get_following):
        can_follow = False
    else:
        can_follow = True
    
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('user_blog_posts.html', user=user, blog_posts=blog_posts, notifs=notifs, can_follow=can_follow)

####################################################
# FOLLOW USER ######################################
####################################################

@users.route("/follow/<user_id_1>/<user_id_2>")
@login_required
def follow(user_id_1, user_id_2):
    user_id_1 = int(user_id_1)
    user_id_2 = int(user_id_2)

    temp = user_id_1

    data = Followers.query.filter_by(follower_id=user_id_1, followed_id=user_id_2).all()

    if (data):
        flash(f"You are already following {user_id_2}")
    else:
        data = Followers(user_id_1, user_id_2)
        db.session.add(data)
        
        notif = Notifications(temp, f'You started following {user_id_2}')
        db.session.add(notif)
        
        db.session.commit()

        flash(f'You are following {user_id_2}!')

    user = User.query.get_or_404(user_id_2)
    return redirect(url_for('user.user_posts', username=user.username))

####################################################
# UNFOLLOW USER ####################################
####################################################

@users.route("/unfollow/<user_id_1>/<user_id_2>")
@login_required
def unfollow(user_id_1, user_id_2):
    user_id_1 = int(user_id_1)
    user_id_2 = int(user_id_2)

    temp = user_id_1

    data = Followers.query.filter_by(follower_id=user_id_1, followed_id=user_id_2).first()

    if (not data):
        flash(f"You don't follow {user_id_2}")
    else:
        db.session.delete(data)
        
        notif = Notifications(temp, f'You stopped following {user_id_2}')
        db.session.add(notif)
        
        db.session.commit()

        flash(f'You unfollowed {user_id_2}!')

    user = User.query.get_or_404(user_id_2)
    return redirect(url_for('user.user_posts', username=user.username))