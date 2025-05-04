from flask import Blueprint

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return "Hello, world!"

@views.route("/about")
def about():
    return "About this app"