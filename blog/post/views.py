####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, url_for, request, redirect, Blueprint, flash, abort
from flask_login import current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db
from blog.models import BlogPost, User, Notifications, Followers, View
from blog.post.forms import BlogPostForm

####################################################
# BLUEPRINT SETUP ##################################
####################################################

blog_posts = Blueprint('blog_posts', __name__)

####################################################
# CREATE POST SETUP ################################
####################################################

@blog_posts.route('/create', methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogPostForm()
    
    if (form.validate_on_submit() or request.method == "POST"):
        post = BlogPost(title=form.title.data, category=form.category.data, text=form.text.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        followers = Followers.query.filter_by(followed_id=current_user.id).all()

        for follower in followers:
            notif = Notifications(follower.follower_id, f'{current_user.username} has posted a blog "{form.title.data}"!', post.id, True)
            db.session.add(notif)

        db.session.add(post)
        db.session.commit()

        flash('Post Created!')
        
        return redirect(url_for('core.index'))

    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('create_post.html', form=form, notifs=notifs)

####################################################
# BLOG POST VIEW SETUP #############################
####################################################

@blog_posts.route('/blog/<int:blog_post_id>')
def blog_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)

    if (current_user.is_authenticated and current_user.email != post.author.email):
        user = User.query.get_or_404(current_user.id)
        user.last_viewed_catagory = post.category
        
        db.session.commit()

        view = View.query.filter_by(user_id=current_user.id, blog_id=blog_post_id).first()

        if (not view):
            post.views += 1
            view = View(current_user.id, blog_post_id)
            db.session.add(view)
            db.session.commit()
    
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('blog_posts.html', title=post.title, date=post.date, post=post, category=post.category, notifs=notifs)

####################################################
# UPDATE POST SETUP ################################
####################################################

@blog_posts.route('/<int:blog_post_id>/update', methods=["GET", "POST"])
@login_required
def update(blog_post_id):
    blog_title = None
    post = BlogPost.query.get_or_404(blog_post_id)

    if (post.author != current_user):
        abort(403)
    
    form = BlogPostForm()
    
    if (form.validate_on_submit() or request.method == "POST"):
        post.title = form.title.data
        post.text= form.text.data
        post.category = form.category.data

        followers = Followers.query.filter_by(followed_id=current_user.id).all()

        for follower in followers:
            notif = Notifications(follower.follower_id, f'{current_user.username} has updated the blog "{blog_title}"!', post.id, True)
            db.session.add(notif)

        db.session.commit()
        flash('Updated Post!')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=post.id))

    if (request.method == "GET"):
        form.title.data = post.title
        blog_title = post.title
        form.text.data = post.text
        form.category.data = post.category
    
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('create_post.html', form=form, notifs=notifs)

####################################################
# DELETE POST SETUP ################################
####################################################

@blog_posts.route('/<int:blog_post_id>/delete', methods=["GET", "POST"])
@login_required
def delete(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)

    if (post.author != current_user):
        abort(403)
    
    followers = Followers.query.filter_by(followed_id=current_user.id).all()

    for follower in followers:
        notif = Notifications(follower.follower_id, f'{current_user.username} has deleted the blog "{post.title}"!', post.author.id, False)
        db.session.add(notif)
    
    db.session.delete(post)
    db.session.commit()

    flash('Post Deleted!')

    return redirect(url_for('core.index'))