def generate_report(tickets):
    report = {
        "total_tickets": len(tickets),
        "by_status": {},
        "by_priority": {},
        "by_category": {},
        "assigned": 0,
        "unassigned": 0,
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        category = ticket["category"]

        report["by_status"][status] = report["by_status"].get(status, 0) + 1
        report["by_priority"][priority] = report["by_priority"].get(priority, 0) + 1
        report["by_category"][category] = report["by_category"].get(category, 0) + 1

        if ticket["assigned_to"]:
            report["assigned"] += 1
        else:
            report["unassigned"] += 1

    return report
