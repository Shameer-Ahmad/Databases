
from flask import Blueprint, session, request, jsonify, render_template, redirect, url_for
from website.db import get_db_connection


restaurants = Blueprint("restaurants", __name__)

# Gets all the restaurants
@restaurants.route("/", methods=["GET"])
def all_restaurants():
    # Get the search parameters from the query string
    restaurant_name = request.args.get("restaurant_name")
    neighborhood = request.args.get("neighborhood")
    cuisine_type = request.args.get("cuisine_type")
    
    conn = get_db_connection()

    # Build SQL query based on whether the user is searching
    query = "SELECT * FROM restaurant WHERE 1=1"
    params = []

    if restaurant_name:
        query += " AND restaurant_name LIKE ?"
        params.append(f"%{restaurant_name}%")

    if neighborhood:
        query += " AND city LIKE ?"
        params.append(f"%{neighborhood}%")

    if cuisine_type:
        query += " AND cuisine_type LIKE ?"
        params.append(f"%{cuisine_type}%")

    # Execute the query with parameters
    cursor = conn.execute(query, params)
    restaurants = cursor.fetchall()
    conn.close()

    return render_template("landing.html", restaurants=restaurants)

# Gets the details of one restaurant using restaurant_id
@restaurants.route("/<int:id>", methods=["GET"])
def restaurant_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the restaurant data
    cursor.execute("SELECT restaurant_name FROM restaurant WHERE restaurant_id = ?", (id,))
    restaurant = cursor.fetchone()

    cursor.close()
    conn.close()

    if not restaurant:
        return "Restaurant not found", 404

    return render_template("restaurant_detail.html", restaurant=restaurant)

@restaurants.route("/create", methods=["GET"])
def create_restaurant_form():
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    return render_template("create_restaurant.html")


@restaurants.route("/create", methods=["POST"])
def create_restaurant():
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    # Get form data
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO restaurant (restaurant_name, street_number, street_name, apt_number, city, state, zip_code, cuisine_type, user_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("restaurant_name"), 
        data.get("street_number"),
        data.get("street_name"),
        data.get("apt_number"),
        data.get("city"),
        data.get("state"),
        data.get("zip_code"),
        data.get("cuisine_type"),
        user_id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("restaurants.manage_restaurants"))

# Deletes a restaurant using restaurant_id
@restaurants.route("/<int:id>", methods=["POST"])
def delete_restaurant(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM restaurant WHERE restaurant_id = ?", (id,))

    conn.commit()
    rows_affected = cur.rowcount
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Restaurant not found"}), 404
    
    return redirect(url_for("restaurants.manage_restaurants"))

@restaurants.route("/manage", methods=["GET", "POST"])
def manage_restaurants():
    # Check if the user is logged in
    user_id = session.get('user_id')

    # If not logged in, redirect to login
    if not user_id:
        return redirect(url_for('auth.login'))

    # Fetch restaurants owned by the logged-in owner
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM restaurant WHERE user_id = ?
    """, (user_id,))
    restaurants = cursor.fetchall()
    cursor.close()
    conn.close()

    # Render the manage restaurants page
    return render_template("manage_restaurants.html", restaurants=restaurants)


@restaurants.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_restaurant(id):
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the restaurant data to prefill the form
    cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = ? AND user_id = ?", (id, user_id))
    restaurant = cursor.fetchone()

    if not restaurant:
        cursor.close()
        conn.close()
        return "Restaurant not found or unauthorized", 404

    # If POST request, update the restaurant
    if request.method == "POST":
        data = request.form

        cursor.execute("""
            UPDATE restaurant 
            SET restaurant_name = ?, street_number = ?, street_name = ?, apt_number = ?, city = ?, state = ?, zip_code = ?, cuisine_type = ? 
            WHERE restaurant_id = ?
        """, (
            data.get("restaurant_name"), 
            data.get("street_number"),
            data.get("street_name"),
            data.get("apt_number"),
            data.get("city"),
            data.get("state"),
            data.get("zip_code"),
            data.get("cuisine_type"),
            id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("restaurants.manage_restaurants"))

    cursor.close()
    conn.close()

    # Render the edit form with pre-filled data
    return render_template("edit_restaurant.html", restaurant=restaurant)
