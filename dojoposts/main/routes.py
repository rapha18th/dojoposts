from flask import Blueprint, render_template
from dojoposts.models import Post

main = Blueprint('main', __name__)

# main route
@main.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    posts.paginate()
    return render_template('index.html', title='Posts:.', posts=posts)
