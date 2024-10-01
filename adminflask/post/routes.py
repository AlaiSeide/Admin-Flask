from flask import Blueprint, render_template

post = Blueprint('post', __name__)

@post.route('/post/<int:post_id>')
def view_post(post_id):
    return render_template('post/view_post.html', post_id=post_id)
