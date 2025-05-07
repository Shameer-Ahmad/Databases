
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from website.db import get_db_connection
events = Blueprint("events", __name__)


# Gets the list of events occuring
@events.route("/")
def list_events():
    conn = get_db_connection()
    events = conn.execute("SELECT event_ID, event_name, date_time FROM event").fetchall()
    conn.close()
    events_list = [dict(row) for row in events]

    return render_template("events.html", events=events_list)

# Allows the user to create a new event
@events.route("/", methods=["POST"])
def create_event():
    
    
    
    name = request.form["event_name"]
    date_time = request.form["date_time"]
    capacity = request.form["capacity"]

    conn = get_db_connection()
   


    conn.execute(
        "INSERT INTO event (event_name, date_time, capacity)VALUES (?, ?, ?)" , 
        (name, date_time, capacity)
        )
    conn.commit()
    conn.close()
    return redirect(url_for("events.list_events"))

# Deletes an existing event
@events.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    conn = get_db_connection()
    events = conn.execute("DELETE FROM event where event_ID = ?", (event_id,))
    conn.commit()
    conn.close()
    return f"deleted event {event_id}"

# Allows user to rsvp to an event
@events.route("/<int:event_id>/rsvp", methods=["POST"])
def rsvp_event(event_id):
    conn = get_db_connection()
    rsvp = conn.execute("INSERT INTO rsvp (user_ID, event_ID) VALUES (?,?)", 
                        (user_id, event_id))
    conn.commit()
    conn.close()
    return f"rsvp to event {event_id} successful"
    
