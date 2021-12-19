from flask import Flask, render_template, abort, request

from app.utils import get_posts, get_post_by_id, get_post_by_user, search_posts


app = Flask(__name__)


@app.route("/")
def all_posts():
    posts = get_posts()
    return render_template("index.html", posts=posts)


@app.route("/posts/<int:post_id>")
def post(post_id):
    post = get_post_by_id(post_id)
    if post is None:
        abort(404)
    return render_template("post.html", post=post)


@app.route("/search")
def search():
    search_str = request.args.get("s") or ''
    posts = search_posts(search_str)
    return render_template("search.html", posts=posts, posts_found_cnt=len(posts))


@app.route("/users/<user_name>")
def user_feed(user_name):
    posts = get_post_by_user(user_name)
    return render_template("user-feed.html", posts=posts)
