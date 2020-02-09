####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, url_for, request, redirect, Blueprint, flash, abort
from flask_login import current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db
from blog.models import BlogPost, User, Notifications, Followers, View, Likes, Comments
from blog.post.forms import BlogPostForm, CommentForm

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

@blog_posts.route('/blog/<int:blog_post_id>', methods=["GET", "POST"])
def blog_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    form = CommentForm()

    previous_comments = Comments.query.filter_by(blog_id=post.id).order_by(Comments.date.desc()).all()

    if (form.validate_on_submit() or request.method == "POST"):
        comment = Comments(blog_post_id, current_user.id, form.text.data)
        db.session.add(comment)

        notif = Notifications(post.author.id, f'{current_user.username} has commented on your blog "{post.title}"!', post.id, True)
        db.session.add(notif)

        db.session.commit()

    if (current_user.is_authenticated and current_user.email != post.author.email):
        user = User.query.get_or_404(current_user.id)
        user.last_viewed_catagory3 = user.last_viewed_catagory2
        user.last_viewed_catagory2 = user.last_viewed_catagory1
        user.last_viewed_catagory1 = post.category
        
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
    
    if (current_user.is_authenticated):
        like_stat = Likes.query.filter_by(user_id=current_user.id, blog_id=blog_post_id).first()
    else:
        like_stat = None

    like_count = db.engine.execute(f'''
        select count(*)
        from Likes
        where blog_id={blog_post_id} and like={1}
    ''')
    dislike_count = db.engine.execute(f'''
        select count(*)
        from Likes
        where blog_id={blog_post_id} and like={0}
    ''')
    like_count = [res[0] for res in like_count][0]
    dislike_count = [res[0] for res in dislike_count][0]
    
    if (like_count == None):
        like_count = 0
    if (dislike_count == None):
        like_count = 0
    
    if (like_stat):
        like_val = like_stat.like
    else:
        like_val = None
    
    return render_template('blog_posts.html', title=post.title, date=post.date, post=post, category=post.category, notifs=notifs, like_val=like_val, like_count=like_count, dislike_count=dislike_count, previous_comments=previous_comments, form=form, User=User)

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

    flash('Blog Deleted!')

    return redirect(url_for('core.index'))

####################################################
# LIKE INTERACTION SETUP ###########################
####################################################

@blog_posts.route('/<int:user_id>/<int:blog_post_id>/<int:like>')
@login_required
def like(user_id, blog_post_id, like):
    post = BlogPost.query.get_or_404(blog_post_id)

    if (not current_user.is_authenticated or post.user_id == current_user.id):
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))

    like_entry = Likes.query.filter_by(user_id=user_id, blog_id=blog_post_id).first()

    blog = BlogPost.query.get_or_404(blog_post_id)
    user = User.query.get_or_404(blog.author.id)
    user_reaction = User.query.get_or_404(user_id)

    if (not like_entry):
        like_entry = Likes(user_id, blog_post_id, bool(like))
        db.session.add(like_entry)

        notif = Notifications(user.id, f'{user_reaction.username} has reacted to your blog "{blog.title}"!', blog_post_id, True)
        db.session.add(notif)
        
        if (like):
            flash('Blog Liked!')
        else:
            flash('Blog Disliked!')

    else:
        if (like_entry.like != bool(like)):
            like_entry.like = bool(like)

            notif = Notifications(user.id, f'{user_reaction.username} has reacted to your blog "{blog.title}"!', blog_post_id, True)
            db.session.add(notif)

            if (like):
                flash('Blog Liked!')
            else:
                flash('Blog Disliked!')
        else:
            db.session.delete(like_entry)
            flash("Reaction Removed")

    db.session.commit()
    
    return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))