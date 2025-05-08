from flask import Blueprint, render_template, session 
from website.db import get_db_connection

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # Fetch all restaurants with neighborhood data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.restaurant_id, r.restaurant_name, r.street_number, r.street_name, 
               r.city, r.state, r.zip_code, r.cuisine_type, nz.neighborhood 
        FROM restaurant r 
        LEFT JOIN neighborhood_zip nz ON r.zip_code = nz.zip_code
    """)
    restaurants = cursor.fetchall()
    conn.close()

    # Fetch user data
    user_id = session.get('user_id')
    user = None

    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

    # Render the landing page with the list of restaurants and user info
    return render_template("landing.html", restaurants=restaurants, user=user)

@views.route("/about")
def about():
    return "About this app"