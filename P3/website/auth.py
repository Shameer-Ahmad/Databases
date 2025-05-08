from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from website.db import get_db_connection

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET"])
def landing_page():
    conn = get_db_connection()
    restaurants = conn.execute("SELECT restaurant_name, street_number, street_name, city, state, zip_code, cuisine_type FROM restaurant").fetchall()
    conn.close()

    # Get the user_id from the session
    user_id = session.get('user_id')

    # Fetch user information
    user = None
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

    # Render the landing page with the list of restaurants and user
    return render_template("landing.html", restaurants=restaurants, user=user)
                
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Log the user in (store user_id in session)
            session['user_id'] = user['user_id']

            # Set is_logged = 1 in the DB
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET is_logged = 1 WHERE user_id = ?", (user['user_id'],))
            conn.commit()
            conn.close()

            return redirect(url_for('auth.landing_page'))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        verification = request.form.get("verification")

        if role == "owner" and verification != current_app.config['VERIFICATION_CODE']:
            return "Wrong verification code", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (username, password, role, is_logged) VALUES (?, ?, ?, ?)",
            (username, password, role, 1)
        )
        # Get the user_id of the inserted user
        user_id = cursor.lastrowid

        conn.commit()
        conn.close()

        # Set user ID in session
        session['user_id'] = user_id

        return redirect(url_for('auth.landing_page'))
    return render_template("register.html")

@auth.route("/logout")
def logout():
    user_id = session.get('user_id')

    if user_id:
        # Update the user's is_logged status in the DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET is_logged = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

        # Remove user from session
        session.pop('user_id', None)

    # Redirect to home or login page (adjust as needed)
    return redirect(url_for('auth.landing_page'))