from flask import Blueprint, request, session, redirect, url_for
from website.db import get_db_connection
from datetime import datetime

reviews = Blueprint("reviews", __name__)

# Creates a new review
@reviews.route("/create_review", methods=["POST"])
def create_review():
    user_id = session.get("user_id")
    text = request.form.get("text")
    score = request.form.get("score")
    restaurant_name = request.form.get("restaurant_name")
    date_time = datetime.now()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO review (user_id, date_time, text, score)
        VALUES (?, ?, ?, ?)
    """, (user_id, date_time, text, score))
    conn.commit()
    conn.close()

    return f"Review submitted by user {user_id} for {restaurant_name}: '{text}' (Score: {score})"
  

# Gets all reviews for a user using user_id
@reviews.route("/my_reviews", methods=["GET"])
def my_reviews():
    return "list of my reviews"

