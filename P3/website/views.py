from flask import Blueprint, render_template, session 
from website.db import get_db_connection

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # Fetch all restaurants from the database
    conn = get_db_connection()
    restaurants = conn.execute("""
        SELECT restaurant_id, restaurant_name, street_number, street_name, city, state, zip_code, cuisine_type 
        FROM restaurant
    """).fetchall()
    conn.close()
    user_id = session.get('user_id')
    user = None
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()


    # Render the landing page with the list of restaurants
    return render_template("landing.html", restaurants=restaurants, user = user)

@views.route("/about")
def about():
    return "About this app"