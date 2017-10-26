from flask import request, redirect, render_template, session, flash
from models import User, BlogPost
from app import db, app
import cgi


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
            print("it worked")
            return redirect("/")
        else:
            return "<h1> You're so stupid </h1>"
    
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
    
        if not username or not password:
            return redirect("/register")
    
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return redirect("/")
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
        return redirect("/")


    return render_template("add-post.html")


@app.route("/all-posts", methods=["GET", "POST"])
# if no request, show all posts from all users
# if user get request, show all user's posts (user-posts template)
# if post get request, show individual post (single-post template)
def show_posts():
    return render_template("all-posts.html")


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