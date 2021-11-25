from flask import Blueprint, render_template, url_for, redirect
from dojoposts.users.forms import Signup, Login, UpdateAccount
from dojoposts import db, bcrypt
from dojoposts.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

users = Blueprint('users', __name__)

# signup route
@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('signup.html', title='Sign up for DojoPosts', form=form)


# login route
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('posts.post'))
    return render_template('login.html', title='Login on Dojo Posts', form=form)


# logout route
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# account route
@users.route('/account')
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
    posts.paginate()
    return render_template('account.html', title='Account', posts=posts)


# update account route
@users.route('/update-account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        return redirect(url_for('users.account'))
    return render_template('update-account.html', title='Update Account', form=form)
