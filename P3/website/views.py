from flask import Blueprint, render_template 
from website.db import get_db_connection

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # Fetch all restaurants from the database
    conn = get_db_connection()
    restaurants = conn.execute("SELECT restaurant_name, street_number, street_name, city, state, zip_code, cuisine_type FROM restaurant").fetchall()
    conn.close()

    # Render the landing page with the list of restaurants
    return render_template("landing.html", restaurants=restaurants)

@views.route("/about")
def about():
    return "About this app"