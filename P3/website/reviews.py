from flask import Blueprint

reviews = Blueprint("reviews", __name__)

@reviews.route("/", methods=["POST"])
def create_review():
    return "create review"

@reviews.route("/mine")
def my_reviews():
    return "my reviews"

@reviews.route("/restaurant/<int:restaurant_id>")
def reviews_for_restaurant(restaurant_id):
    return f"reviews for restaurant {restaurant_id}"
