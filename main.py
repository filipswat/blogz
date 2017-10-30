from flask import request, redirect, render_template, session, flash
from models import User, BlogPost
from app import db, app
import cgi

def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

@app.route("/login", methods = ["GET", "POST"])
# link to registration page at bottom
def login():
    # retrieve form data
    # confirm username exists, matches password
    # add name to session
    # redirect to home page

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="this is an error")
    
    return render_template("login.html")


@app.route("/register", methods = ["GET", "POST"])
# most straightforward -- check for username uniqueness, check passwords match
def register():
    # validate name (exists, not a user) and password (exists, verified)
    # add name to session
    # redirect to home page

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]
    
        if not username or not password or not password==verify:
            return render_template("register.html", error="this is an error")
    
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return redirect("/add-post")
        else:
            return redirect("/login")
        
    return render_template("register.html")


@app.route("/add-post", methods=["GET", "POST"])
# if user not logged in, redirect to login page, else display form
# if form submitted, add post to db, redirect to all-posts to display post
def add_post():
    # if not logged in, redirect

    if "username" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        username = session["username"]
        title = request.form["title"]
        content = request.form["content"]

        if not title or not content:
            return redirect("/add-post")
        
        user = User.query.filter_by(username=username).first()

        new_post = BlogPost(title, content, user)
        db.session.add(new_post)
        db.session.commit()

        return render_template("single-post.html",
        post=new_post, user=user)


    return render_template("add-post.html")


@app.route("/all-posts", methods=["GET"])
# if no request, show all posts from all users
# if user get request, show all user's posts (user-posts template)
# if post get request, show individual post (single-post template)
def show_posts():
    get_user = request.args.get("user-id")
    get_post = request.args.get("post-id")

    post_list = BlogPost.query.all()

    if get_user:
        if not is_int(get_user):
            return render_template("all-posts.html", post_list=post_list)
        
        user_id = int(get_user)
        post_list = BlogPost.query.filter_by(creator_id=user_id).all()

        return render_template("all-posts.html", post_list=post_list)
    
    if get_post:
        if not is_int(get_post):
            return render_template("all-posts.html", post_list=post_list)
        
        post_id = int(get_post)
        post = BlogPost.query.get(post_id)
        user = User.query.get(post.creator_id)

        return render_template("single-post.html", post=post, user=user)

    return render_template("all-posts.html", post_list=post_list)


@app.route("/logout")
# ends session, opens up all-posts page
def logout():
    if "username" in session:
        del session["username"]
    return redirect("/")


@app.route("/")
# show list of all users
def index():
    user_list = User.query.all()

    return render_template("all-users.html", user_list=user_list)

if __name__ == "__main__":
    app.run()