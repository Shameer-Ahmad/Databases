from flask import Blueprint

events = Blueprint("events", __name__)

@events.route("/")
def list_events():
    return "list of events"

@events.route("/", methods=["POST"])
def create_event():
    return "create event"

@events.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    return f"delete event {event_id}"

@events.route("/<int:event_id>/rsvp", methods=["POST"])
def rsvp_event(event_id):
    return f"rsvp to event {event_id}"
