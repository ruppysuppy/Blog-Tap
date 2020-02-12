####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, url_for, flash, redirect, request, Blueprint, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db, mail
from blog.models import User, BlogPost, Notifications, Followers
from blog.users.forms import Register, UpdateUserForm, LoginForm, ForgotPasswordForm, ChangePasswordForm, UpdatePasswordForm
from blog.users.password import is_strong

####################################################
# BLUEPRINT SETUP ##################################
####################################################

users = Blueprint('user', __name__)

####################################################
# TIMED SERIALIZER SETUP ###########################
####################################################

serializer = URLSafeTimedSerializer('somesecretkey')

####################################################
# REGISTRATION SETUP ###############################
####################################################

@users.route('/register', methods=["GET", "POST"])
def register():
    form = Register()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if (user == None):
            if (is_strong(form.password.data)):
                user = User(email=form.email.data, username=form.username.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()

                try:
                    token = serializer.dumps(form.email.data, salt='email-confirm')
                    link = url_for('user.confirm_email', token=token, _external=True)
                    link_home = url_for('core.index', _external=True)

                    msg = Message('Blog Tap Email Confirmation', sender='tap@blogtap.com', recipients=[form.email.data])

                    msg.body = f'''
\tWelcome Blogger!

{form.username.data}, thankyou for registering at Blog Tap. 
Please click on the link below to confirm your email id.
Your confirmation link is: {link}
Login to your account and start Blogging at Blog Tap ({link_home}).
Hope you have an awesome time.
        
\tYour Sincerely
\tTapajyoti Bose
\tCreator
\tBlog Tap
'''

                    mail.send(msg)

                    flash(f'Thankyou for registering at Blog Tap. Welcome {form.username.data}! Please confirm your email within 30 days.')

                    return redirect(url_for('user.login'))

                except:
                    flash('Your Account has been created, but we were unable to send the confirmation mail.')
                    return redirect(url_for('user.login'))

            else:
                flash('Use a strong password (1 Upper and 1 lower case characters, 1 number, 1 symbol and minimum length of 6)')
                return redirect(url_for('user.register'))
        
        else:
            flash('Email already registered!')
            return redirect(url_for('user.register'))
    
    return render_template('register.html', form=form)

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
    
    return render_template('login.html', form=form)

####################################################
# LOGOUT SETUP #####################################
####################################################

@users.route('/logout')
@login_required
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

        flash('Username Updated!')

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

@users.route("/user/<int:user_id>")
def user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=user_id).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.views.desc(), BlogPost.date.desc()).paginate(page=page, per_page=6)

    followers_count = db.engine.execute(f"select count(*) as count   \
                                          from Followers             \
                                          where followed_id={user.id}").scalar()

    if (current_user.is_authenticated):
        get_following = Followers.query.filter(Followers.follower_id==current_user.id, Followers.followed_id==user.id).first()
        if (get_following):
            can_follow = False
        else:
            can_follow = True
    else:
        get_following = False
        can_follow = False
    
    if (current_user.is_authenticated):
        notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()
    else:
        notifs = []

    return render_template('user_blog_posts.html', user=user, blog_posts=blog_posts, notifs=notifs, can_follow=can_follow, followers_count=followers_count)

####################################################
# FOLLOW USER ######################################
####################################################

@users.route("/follow/<int:user_id_1>/<int:user_id_2>")
@login_required
def follow(user_id_1, user_id_2):
    data = Followers.query.filter_by(follower_id=user_id_1, followed_id=user_id_2).all()

    if (data):
        flash(f"You are already following {user_id_2}!")
    else:
        data = Followers(user_id_1, user_id_2)
        db.session.add(data)
        
        notif = Notifications(user_id_1, f'You started following {user_id_2}!', user_id_2, False)
        db.session.add(notif)
        
        db.session.commit()

        flash(f'You are following {user_id_2}!')

    user = User.query.get_or_404(user_id_2)
    return redirect(url_for('user.user_posts', user_id=user.id))

####################################################
# UNFOLLOW USER ####################################
####################################################

@users.route("/unfollow/<int:user_id_1>/<int:user_id_2>")
@login_required
def unfollow(user_id_1, user_id_2):
    data = Followers.query.filter_by(follower_id=user_id_1, followed_id=user_id_2).first()

    if (not data):
        flash(f"You don't follow {user_id_2}!")
    else:
        db.session.delete(data)
        
        notif = Notifications(user_id_1, f'You stopped following {user_id_2}!', user_id_2, False)
        db.session.add(notif)
        
        db.session.commit()

        flash(f'You unfollowed {user_id_2}!')

    user = User.query.get_or_404(user_id_2)
    return redirect(url_for('user.user_posts', user_id=user.id))

####################################################
# EMAIL CONFIRMATION SETUP #########################
####################################################

@users.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=(86400 * 30))
        user = User.query.filter_by(email=email).first()
        user.confirmed = True
        db.session.commit()

    except SignatureExpired:
        email = serializer.loads(token, salt='email-confirm')
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()

        flash('Activation Link has expired. Your account was deleted. Please create your account again and confirm the email id as soon as possible!')
        return redirect(url_for('user.register'))
    
    except:
        flash('Invalid Token')
        return redirect(url_for('core.index'))
    
    flash('Email id Confirmed! Start blogging Now!')
    return redirect(url_for('user.account'))

####################################################
# CHANGE BACKGROUND ################################
####################################################

@users.route("/change-background")
@login_required
def change_background():
    user = User.query.get_or_404(current_user.id)
    background_img_num = int(user.background)
    
    background_img_num = (background_img_num + 1) % 7
    
    if (background_img_num == 0):
        background_img_num = 1
    
    user.background = str(background_img_num)
    db.session.commit()
    
    return redirect(url_for('user.account'))

####################################################
# FORGOT PASSWORD SETUP ############################
####################################################

@users.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if (form.validate_on_submit() or request.method == "POST"):
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if (not user):
            flash("There is no account registered using this email id")
            return redirect(url_for('user.register'))
        else:
            if (not user.confirmed):
                db.session.delete(user)
                db.session.commit()

                flash("You had not confirmed your email. Your account has been deleted. Please re-open a new account.")
                return redirect(url_for('user.register'))
            else:
                try:
                    token = serializer.dumps(email, salt='forgot-confirm')
                    link = url_for('user.change_password', token=token, _external=True)

                    msg = Message('Blog Tap Password Reset', sender='tap@blogtap.com', recipients=[email])

                    msg.body = f'''
\tWelcome Blogger!

Hello {user.username}.
Please click on the link below to reset your password at Blog Tap.
Your reset link is: {link}
If you didn't request password reset, please ignore this mail.
Hope you have an awesome time.
        
\tYour Sincerely
\tTapajyoti Bose
\tCreator
\tBlog Tap
'''

                    mail.send(msg)

                    flash(f'Password reset mail has been sent. Please reset your password within 48 hours.')
                    return redirect(url_for('user.login'))

                except:
                    flash('We were unable to send the password reset mail.')
                    return redirect(url_for('core.index'))
    
    return render_template('forgot-pass.html', form=form)

####################################################
# RESET PASSWORD  ##################################
####################################################

@users.route("/change-password/<token>", methods=["GET", "POST"])
def change_password(token):
    try:
        email = serializer.loads(token, salt='forgot-confirm', max_age=(86400 * 2))
        user = User.query.filter_by(email=email).first()

        login_user(user)
        session.permanent = True

        form = ChangePasswordForm()

        if (form.validate_on_submit() or request.method == "POST"):
            if (is_strong(form.password.data)):
                pswrd = User.gen_pass(form.password.data)
                user.password_hash = pswrd
                db.session.commit()

                flash("Password Reset!")
                return redirect(url_for('core.index'))
            else:
                flash("Use a strong password (1 Upper and 1 lower case characters, 1 number, 1 symbol and minimum length of 6)")
                return redirect(url_for('user.change_password', token=token))

    except SignatureExpired:
        email = serializer.loads(token, salt='forgot-confirm')
        user = User.query.filter_by(email=email).first()

        flash('Activation Link has expired. Please create go through the "Forgot Password" Process again!')
        return redirect(url_for('user.forgot_password'))
    
    except:
        flash('Invalid Token')
        return redirect(url_for('core.index'))
    
    return render_template('pass-reset.html', form=form)

####################################################
# UPDATE PASSWORD  #################################
####################################################

@users.route("/update-password", methods=["GET", "POST"])
@login_required
def update_password():
    form = UpdatePasswordForm()

    if (form.validate_on_submit() or request.method == "POST"):
        user = User.query.get_or_404(current_user.id)
        
        if (user.check_password(form.curr_pass.data)):
            if (is_strong(form.password.data)):
                user.password_hash = User.gen_pass(form.password.data)
                db.session.commit()
                flash('Password Updated!')
                return redirect(url_for('user.account'))

            else:
                flash('Use a strong password (1 Upper and 1 lower case characters, 1 number, 1 symbol and minimum length of 6)')
                return redirect(url_for('user.update_password'))

        else:
            flash("Incorrect Password!")
            return redirect(url_for('user.update_password'))
    
    notifs = Notifications.query.filter_by(user_id=current_user.id).order_by(Notifications.date.desc()).all()

    return render_template('update-pass.html', form=form, notifs=notifs)