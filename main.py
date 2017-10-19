from flask import request, redirect, render_template, session, flash
from models import User, BlogPost
from app import db, app
import cgi