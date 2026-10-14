import json
from campusflow.tickets import (
    CATEGORIES, URGENCIES, STATUSES, calculate_priority
)


def validate_tickets(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Invalid ticket data")

    ids = set()

    for t in tickets:
        required = [
            "id", "title", "category", "urgency", "affected_users",
            "priority", "status", "assigned_to", "notes"
        ]
        if not isinstance(t, dict) or not all(k in t for k in required):
            raise ValueError("Invalid ticket structure")

        if type(t["id"]) != int or t["id"] <= 0 or t["id"] in ids:
            raise ValueError("Invalid or duplicate ticket ID")
        ids.add(t["id"])

        if not isinstance(t["title"], str) or not t["title"].strip():
            raise ValueError("Invalid title")
        if t["category"] not in CATEGORIES:
            raise ValueError("Invalid category")
        if t["urgency"] not in URGENCIES:
            raise ValueError("Invalid urgency")
        if type(t["affected_users"]) != int or t["affected_users"] <= 0:
            raise ValueError("Invalid affected users")
        if t["priority"] != calculate_priority(t["urgency"], t["affected_users"]):
            raise ValueError("Incorrect priority")
        if t["status"] not in STATUSES:
            raise ValueError("Invalid status")
        if t["assigned_to"] is not None and (
            not isinstance(t["assigned_to"], str) or not t["assigned_to"].strip()
        ):
            raise ValueError("Invalid assignment")
        if not isinstance(t["notes"], list):
            raise ValueError("Invalid notes")

        note_ids = set()
        for n in t["notes"]:
            if not isinstance(n, dict) or not all(
                k in n for k in ("note_id", "author", "message")
            ):
                raise ValueError("Invalid note")
            note_id = n["note_id"]
            if (
                not isinstance(note_id, str) or len(note_id) != 4
                or not note_id.startswith("N") or not note_id[1:].isdigit()
                or int(note_id[1:]) < 1 or note_id in note_ids
            ):
                raise ValueError("Invalid or duplicate note ID")
            note_ids.add(note_id)
            if not isinstance(n["author"], str) or not n["author"].strip():
                raise ValueError("Invalid note author")
            if not isinstance(n["message"], str) or not 5 <= len(n["message"].strip()) <= 300:
                raise ValueError("Invalid note message")


def save_tickets(path, tickets):
    validate_tickets(tickets)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)


def load_tickets(path):
    with open(path, encoding="utf-8") as file:
        tickets = json.load(file)
    validate_tickets(tickets)
    return tickets