from flask import Blueprint, request, jsonify
from website.db import get_db_connection

reviews = Blueprint("reviews", __name__)

# Creates a new review
@reviews.route("/", methods=["POST"])
def create_review():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO review (user_id, restaurant_id, date_time, text, score) 
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("user_id"), ### User ID will need to be updated -> TAKE OUT
        data.get("restaurant_id"), 
        data.get("date_time"),
        data.get("text"),
        data.get("score")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Review added successfully!",
        "user_ID": data.get("user_ID"), ### User ID will need to be updated -> TAKE OUT
        "date_time": data.get("date_time")
    }), 201

# Gets all reviews for a user using user_id
@reviews.route("/mine", methods=["GET"])
def my_reviews():
    #user_id = request.args.get("user_id")  ### User ID will need to be updated -> TAKE OUT
    user_id = 5  # For testing purposes, hardcoded user_id to 5 -> TAKE OUT

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400 ### User ID will need to be updated -> TAKE OUT
    
    conn = get_db_connection()
    cur  = conn.cursor()
    reviews = cur.execute("SELECT * FROM review WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()

    if not reviews:
        return jsonify({"error": "No reviews found for this user"}), 404

    return jsonify([dict(review) for review in reviews])

# Gets all reviews for a restaurant using restaurant_id
@reviews.route("/restaurant/<int:restaurant_id>", methods=["GET"])
def reviews_for_restaurant(restaurant_id):
    conn = get_db_connection()
    cur = conn.cursor()
    reviews = cur.execute("SELECT * FROM review WHERE restaurant_id = ?", (restaurant_id,)).fetchall()
    conn.close()

    if not reviews:
        return jsonify({"error": "No reviews found for this restaurant"}), 404

    return jsonify([dict(review) for review in reviews])
