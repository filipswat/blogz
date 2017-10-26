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
    return render_template("login.html")


@app.route("/register", methods = ["GET", "POST"])
# most straightforward -- check for username uniqueness, check passwords match
def register():
    # retrieve form data
    # validate name (exists, unique) and password (exists, verified)
    # add name to session
    # redirect to home page
    return render_template("register.html")


@app.route("/add-post")
# if user not logged in, redirect to login page, else display form
def add_post():
    # if not logged in, redirect
    return render_template("add-post.html")


@app.route("/all-posts", methods=["GET"])
# if no request, show all posts from all users
# if user get request, show all user's posts (user-posts template)
# if post get request, show individual post (single-post template)
def show_posts():
    return render_template("all-posts.html")


@app.route("/logout")
# ends session, opens up all-posts page
def logout():
    return redirect("/")


@app.route("/")
# show list of all users
def index():
    user_list = User.query.all()

    return render_template("all-users.html", user_list=user_list)

if __name__ == "__main__":
    app.run()