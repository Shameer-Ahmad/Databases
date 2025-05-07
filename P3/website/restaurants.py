
from flask import Blueprint, request, jsonify, render_template, redirect, url_for 
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

    restaurant = conn.execute("SELECT * FROM restaurant WHERE restaurant_id = ?", (id,)).fetchone()

    conn.close()

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404

    return jsonify(dict(restaurant))

@restaurants.route("/create", methods=["GET"])
def create_restaurant_form():
    return render_template("create_restaurant.html")

# Creates a new restaurant (POST request)
@restaurants.route("/create", methods=["POST"])
def create_restaurant():
    # Get form data
    data = request.form  # For form submissions
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO restaurant (restaurant_name, street_number, street_name, apt_number, city, state, zip_code, cuisine_type) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("restaurant_name"), 
        data.get("street_number"),
        data.get("street_name"),
        data.get("apt_number"),
        data.get("city"),
        data.get("state"),
        data.get("zip_code"),
        data.get("cuisine_type")
    ))

    conn.commit()
    new_restaurant_id = cur.lastrowid  # Get the ID of the newly inserted restaurant
    conn.close()

    return redirect(url_for("restaurants.all_restaurants"))  # Or redirect to any page you want


# Updates a restaurant using restaurant_id
@restaurants.route("/<int:id>", methods=["PUT"])
def update_restaurant(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
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
    conn.close()

    return jsonify({"message": "Restaurant updated successfully!"})

# Deletes a restaurant using restaurant_id
@restaurants.route("/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM restaurant WHERE restaurant_id = ?", (id,))

    conn.commit()
    rows_affected = cur.rowcount
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Restaurant not found"}), 404
    
    return jsonify({"message": "Restaurant deleted successfully!"})


#Restaurant Search 
