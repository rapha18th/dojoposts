from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from dojoposts.posts.forms import PostForm
from dojoposts import db
from dojoposts.models import Post, User
from flask_login import current_user

posts = Blueprint('posts', __name__)

# posts route
@posts.route('/posts', methods=['GET', 'POST'])
@login_required
def post():
    posts = Post.query.order_by(Post.date_posted.desc())
    posts.paginate()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post_content=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.post'))
    return render_template('posts.html', title='posts', posts=posts, form=form)


# user post
@posts.route('/user-post/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
    posts.paginate()
    if user == current_user:
        return redirect(url_for('users.account'))
    return render_template('user-posts.html', title='User Posts', posts=posts, user=user)
