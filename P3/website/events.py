
from flask import Blueprint, request, jsonify
from website.db import get_db_connection
events = Blueprint("events", __name__)


# Gets the list of events occuring
@events.route("/")
def list_events():
    conn = get_db_connection()
    events = conn.execute("SELECT event_ID, date_time FROM event").fetchall()
    conn.close()
    results = [dict(row) for row in events]

    return jsonify(results)

# Allows the user to create a new event
@events.route("/", methods=["POST"])
def create_event():
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO event (event_ID, date_time, capacity)
        VALUES (?, ?, ?)
    """, (
        data.get("event_ID"), 
        data.get("date_time"),
        data.get("capacity"),
    ))
    conn.commit()
    conn.close()
    return "event created"

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
    
