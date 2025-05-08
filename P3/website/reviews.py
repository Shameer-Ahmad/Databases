from flask import Blueprint, request, session, redirect, url_for, flash 
from website.db import get_db_connection
from datetime import datetime

reviews = Blueprint("reviews", __name__)

# Creates a new review
@reviews.route("/create_review", methods=["POST"])
def create_review():
    user_id = session.get("user_id")
    text = request.form.get("text")
    score = request.form.get("score")
    restaurant_id = request.form.get("restaurant_id")
    date_time = datetime.now()

    if not user_id:
        flash("You must be logged in to leave a review.", "error")
        return redirect(url_for("views.home"))

    if not restaurant_id:
        flash("Invalid restaurant.", "error")
        return redirect(url_for("views.home"))

    # Insert review
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO review (user_id, restaurant_id, date_time, text, score)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, restaurant_id, date_time, text, score))
    
    conn.commit()
    conn.close()

    flash("Review successfully submitted!", "success")
    return redirect(url_for("views.home"))

# Gets all reviews for a user using user_id
@reviews.route("/my_reviews", methods=["GET"])
def my_reviews():
    return "list of my reviews"

