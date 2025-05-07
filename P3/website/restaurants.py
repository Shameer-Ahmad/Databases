
from flask import Blueprint, request, jsonify, render_template, redirect, url_for 
from website.db import get_db_connection

restaurants = Blueprint("restaurants", __name__)

# Gets all the restaurants
@restaurants.route("/", methods=["GET"])
def all_restaurants():
    conn = get_db_connection()
    restaurants = conn.execute("SELECT restaurant_name FROM restaurant").fetchall()
    conn.close()

    results = [dict(row) for row in restaurants]

    return jsonify(results)

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
