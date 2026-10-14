CATEGORIES = ["Network", "Hardware", "Software", "Other"]
URGENCIES = ["low", "medium", "high"]
STATUSES = ["open", "in_progress", "resolved"]


def calculate_priority(urgency, users):
    if urgency == "high" and users >= 10:
        return "critical"
    if urgency == "high" or users >= 10:
        return "high"
    if urgency == "medium" or users >= 3:
        return "medium"
    return "low"


def create_ticket(tickets, title, category, urgency, users):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Invalid title")
    if not isinstance(category, str) or category.strip().title() not in CATEGORIES:
        raise ValueError("Invalid category")
    if not isinstance(urgency, str) or urgency.strip().lower() not in URGENCIES:
        raise ValueError("Invalid urgency")
    if type(users) != int or users <= 0:
        raise ValueError("Invalid number of users")

    ticket = {
        "id": max((t["id"] for t in tickets), default=0) + 1,
        "title": title.strip(),
        "category": category.strip().title(),
        "urgency": urgency.strip().lower(),
        "affected_users": users,
        "priority": calculate_priority(urgency.strip().lower(), users),
        "status": "open",
        "assigned_to": None,
        "notes": []
    }
    tickets.append(ticket)
    return ticket


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ValueError("Ticket not found")


def assign_ticket(tickets, ticket_id, staff):
    ticket = find_ticket(tickets, ticket_id)
    if ticket["status"] == "resolved":
        raise ValueError("Ticket is resolved")
    if not isinstance(staff, str) or not staff.strip():
        raise ValueError("Invalid staff name")
    ticket["assigned_to"] = staff.strip()


def change_status(tickets, ticket_id, status):
    ticket = find_ticket(tickets, ticket_id)
    allowed = {
        "open": ["in_progress", "resolved"],
        "in_progress": ["resolved"],
        "resolved": ["open"]
    }

    if status not in STATUSES or status not in allowed[ticket["status"]]:
        raise ValueError("Invalid status change")
    if status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign ticket first")

    ticket["status"] = status


def add_note(tickets, ticket_id, author, message):
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Reopen ticket first")
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Invalid author")
    if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
        raise ValueError("Note must be 5–300 characters")

    number = max(
        (int(n["note_id"][1:]) for n in ticket["notes"]),
        default=0
    ) + 1

    note = {
        "note_id": f"N{number:03d}",
        "author": author.strip(),
        "message": message.strip()
    }
    ticket["notes"].append(note)
    return note


def view_notes(tickets, ticket_id):
    return sorted(
        find_ticket(tickets, ticket_id)["notes"],
        key=lambda n: int(n["note_id"][1:])
    )


def open_work_queue(tickets):
    order = {"critical": 1, "high": 2, "medium": 3, "low": 4}
    return sorted(
        [t for t in tickets if t["status"] == "open"],
        key=lambda t: (order[t["priority"]], t["id"])
    )


def search_tickets(tickets, query):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty")

    query = query.strip().lower()

    return [
        ticket for ticket in tickets
        if query in ticket["title"].lower()
        or query in ticket["category"].lower()
        or query in ticket["status"].lower()
    ]