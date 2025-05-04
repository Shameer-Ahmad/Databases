from flask import Blueprint

restaurants = Blueprint("restaurants", __name__)

@restaurants.route("/")
def all_restaurants():
    return "all restaurants"

@restaurants.route("/<int:id>")
def restaurant_detail(id):
    return f"restaurant detail for {id}"