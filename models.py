from app import db
from flask import request, redirect, render_template, session, flash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship("BlogPost", backref="creator")

    def __init__(self, email, password):
        self.email = email
        self.password = password

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(6000))
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __init__(self, title, content, creator):
        self.title = title
        self.content = content
        self.creator = creator