from flask import Blueprint, session, request, jsonify, render_template, redirect, url_for
from website.db import get_db_connection
from datetime import datetime

restaurants = Blueprint("restaurants", __name__)

# Gets all the restaurants
@restaurants.route("/", methods=["GET"])
def all_restaurants():
    # Get search parameters from the query string
    restaurant_name = request.args.get("restaurant_name")
    neighborhood = request.args.get("neighborhood")
    cuisine_type = request.args.get("cuisine_type")
    zip_code = request.args.get("zip_code")
    
    conn = get_db_connection()

    # Build SQL query
    query = """
        SELECT r.restaurant_id, r.restaurant_name, r.street_number, r.street_name, 
               r.city, r.state, r.zip_code, r.cuisine_type, nz.neighborhood 
        FROM restaurant r 
        LEFT JOIN neighborhood_zip nz ON r.zip_code = nz.zip_code
        WHERE 1=1
    """
    params = []

    # Apply filters based on provided query parameters
    if restaurant_name:
        query += " AND r.restaurant_name LIKE ?"
        params.append(f"%{restaurant_name}%")

    if neighborhood:
        query += " AND nz.neighborhood LIKE ?"
        params.append(f"%{neighborhood}%")

    if cuisine_type:
        query += " AND r.cuisine_type LIKE ?"
        params.append(f"%{cuisine_type}%")

    if zip_code:
        query += " AND r.zip_code LIKE ?"
        params.append(f"%{zip_code}%")

    # Execute query and fetch data
    cursor = conn.execute(query, params)
    restaurants = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # Render the landing page with the list of restaurants
    return render_template("landing.html", restaurants=restaurants)


# Gets the details of one restaurant using restaurant_id
from datetime import datetime

@restaurants.route("/restaurant/<int:id>", methods=["GET"])
def restaurant_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch restaurant details
    cursor.execute("""
        SELECT r.*, nz.neighborhood 
        FROM restaurant r 
        LEFT JOIN neighborhood_zip nz ON r.zip_code = nz.zip_code 
        WHERE r.restaurant_id = ?
    """, (id,))
    restaurant = cursor.fetchone()

    if not restaurant:
        cursor.close()
        conn.close()
        return "Restaurant not found", 404

    # Fetch events associated with the restaurant
    cursor.execute("""
        SELECT event_ID, event_name, date_time, capacity 
        FROM event 
        WHERE restaurant_id = ?
    """, (id,))
    events = cursor.fetchall()

    # Fetch RSVPs for the events
    cursor.execute("""
        SELECT event_ID, COUNT(user_ID) AS rsvp_count 
        FROM rsvp 
        WHERE event_ID IN (SELECT event_ID FROM event WHERE restaurant_id = ?)
        GROUP BY event_ID
    """, (id,))
    rsvp_counts = cursor.fetchall()

    # Create a dictionary for RSVP counts
    rsvp_dict = {rsvp["event_ID"]: rsvp["rsvp_count"] for rsvp in rsvp_counts}

    # Format event dates
    events_list = []
    for event in events:
        try:
            # Convert date_time to datetime object
            date_obj = datetime.strptime(event["date_time"], "%Y-%m-%dT%H:%M")
            # Format as "May 10th, 2025 - 2:30 PM"
            day = date_obj.day
            suffix = 'th' if 10 <= day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
            formatted_date = date_obj.strftime(f"%B {day}{suffix}, %Y - %I:%M %p")
        except ValueError:
            formatted_date = event["date_time"]  # Keep original format if parsing fails

        events_list.append({
            "event_ID": event["event_ID"],
            "event_name": event["event_name"],
            "formatted_date": formatted_date,
            "capacity": event["capacity"],
            "rsvp_count": rsvp_dict.get(event["event_ID"], 0)
        })

    # Fetch reviews for the restaurant
    cursor.execute("""
        SELECT r.text, r.score, r.date_time, u.username 
        FROM review r
        JOIN user u ON r.user_id = u.user_id
        WHERE r.restaurant_id = ?
        ORDER BY r.date_time DESC
    """, (id,))
    reviews = cursor.fetchall()

    # Format review dates
    reviews_list = []
    for review in reviews:
        try:
            date_obj = datetime.strptime(review["date_time"], "%Y-%m-%d %H:%M:%S.%f")
            day = date_obj.day
            suffix = 'th' if 10 <= day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
            formatted_date = date_obj.strftime(f"%B {day}{suffix}, %Y - %I:%M %p")
        except ValueError:
            formatted_date = review["date_time"]

        reviews_list.append({
            "username": review["username"],
            "text": review["text"],
            "score": review["score"],
            "formatted_date": formatted_date
        })

    # Fetch user data
    user_id = session.get('user_id')
    user = None

    if user_id:
        cursor.execute("""
            SELECT user_id, username, role, is_logged 
            FROM user 
            WHERE user_id = ?
        """, (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            user = {
                "user_id": user_data["user_id"],
                "username": user_data["username"],
                "role": user_data["role"],
                "is_logged": bool(user_data["is_logged"])
            }

    cursor.close()
    conn.close()

    return render_template(
        "restaurant_detail.html",
        restaurant=restaurant,
        events=events_list,
        reviews=reviews_list,
        user=user
    )

@restaurants.route("/create", methods=["GET", "POST"])
def create_restaurant():
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        # Get form data
        data = request.form
        restaurant_name = data.get("restaurant_name")
        street_number = data.get("street_number")
        street_name = data.get("street_name")
        apt_number = data.get("apt_number")
        city = data.get("city")
        state = data.get("state")
        zip_code = data.get("zip_code")
        neighborhood = data.get("neighborhood")
        cuisine_type = data.get("cuisine_type")

        # Check if the neighborhood-zip mapping exists
        cursor.execute("SELECT * FROM neighborhood_zip WHERE zip_code = ?", (zip_code,))
        existing_mapping = cursor.fetchone()

        # If not, insert a new neighborhood-zip mapping
        if not existing_mapping:
            cursor.execute("""
                INSERT INTO neighborhood_zip (zip_code, neighborhood) 
                VALUES (?, ?)
            """, (zip_code, neighborhood))

        # Insert restaurant
        cursor.execute("""
            INSERT INTO restaurant (restaurant_name, street_number, street_name, apt_number, city, state, zip_code, cuisine_type, user_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            restaurant_name, 
            street_number, 
            street_name, 
            apt_number, 
            city, 
            state, 
            zip_code, 
            cuisine_type, 
            user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("restaurants.manage_restaurants"))

    cursor.close()
    conn.close()

    # If GET request, render the create form
    return render_template("create_restaurant.html")


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

    # Fetch the restaurant data to prefill the form, including neighborhood from the join
    cursor.execute("""
        SELECT r.*, nz.neighborhood 
        FROM restaurant r 
        LEFT JOIN neighborhood_zip nz ON r.zip_code = nz.zip_code 
        WHERE r.restaurant_id = ? AND r.user_id = ?
    """, (id, user_id))
    
    restaurant = cursor.fetchone()

    if not restaurant:
        cursor.close()
        conn.close()
        return "Restaurant not found or unauthorized", 404

    # If POST request, update the restaurant
    if request.method == "POST":
        data = request.form

        restaurant_name = data.get("restaurant_name")
        street_number = data.get("street_number")
        street_name = data.get("street_name")
        apt_number = data.get("apt_number")
        city = data.get("city")
        state = data.get("state")
        zip_code = data.get("zip_code")
        neighborhood = data.get("neighborhood")
        cuisine_type = data.get("cuisine_type")

        # Check for existing neighborhood-zip mapping
        cursor.execute("SELECT * FROM neighborhood_zip WHERE zip_code = ?", (zip_code,))
        existing_mapping = cursor.fetchone()

        # If no mapping exists, insert new neighborhood-zip mapping
        if not existing_mapping:
            cursor.execute("""
                INSERT INTO neighborhood_zip (zip_code, neighborhood) 
                VALUES (?, ?)
            """, (zip_code, neighborhood))
        else:
            # If mapping exists, update the neighborhood
            cursor.execute("""
                UPDATE neighborhood_zip 
                SET neighborhood = ? 
                WHERE zip_code = ?
            """, (neighborhood, zip_code))

        # Update the restaurant details
        cursor.execute("""
            UPDATE restaurant 
            SET restaurant_name = ?, street_number = ?, street_name = ?, apt_number = ?, 
                city = ?, state = ?, zip_code = ?, cuisine_type = ? 
            WHERE restaurant_id = ?
        """, (
            restaurant_name,
            street_number,
            street_name,
            apt_number,
            city,
            state,
            zip_code,
            cuisine_type,
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
