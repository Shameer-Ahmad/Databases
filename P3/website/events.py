
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from website.db import get_db_connection
from datetime import datetime
events = Blueprint("events", __name__)

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

# Gets the list of events occuring
@events.route("/")
def list_events():
    conn = get_db_connection()
    events = conn.execute("SELECT event_ID, event_name, date_time, capacity FROM event").fetchall()
    conn.close()
    
    events_list = []
    for event in events:
        event_dict = dict(event)
        
        # Convert the date_time to a datetime object using the correct format (with 'T')
        event_dict['date_time'] = datetime.strptime(event_dict['date_time'], '%Y-%m-%dT%H:%M')  # Corrected format
        
        # Format the date_time as 'May 9th, 2025'
        day = event_dict['date_time'].day
        suffix = 'th' if 10 <= day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        event_dict['formatted_date'] = event_dict['date_time'].strftime(f'%B {day}{suffix}, %Y')
        
        events_list.append(event_dict)

    return render_template("events.html", events=events_list)
# Deletes an existing event
#@events.route("/<int:event_id>", methods=["DELETE"])
@events.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM event WHERE event_ID = ?", (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("events.list_events"))  # Redirect after deletion

# Allows user to rsvp to an event
@events.route("/<int:event_id>/rsvp", methods=["POST"])
def rsvp_event(event_id):
    conn = get_db_connection()
    rsvp = conn.execute("INSERT INTO rsvp (user_ID, event_ID) VALUES (?,?)", 
                        (user_id, event_id))
    conn.commit()
    conn.close()
    return f"rsvp to event {event_id} successful"
    
