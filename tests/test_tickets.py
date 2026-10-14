import unittest
from campusflow.tickets import *


class TestTickets(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def create(self, title="Wi-Fi issue", urgency="high", users=10):
        return create_ticket(self.tickets, title, "Network", urgency, users)

    def test_priority(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("medium", 3), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_invalid_ticket(self):
        for users in (0, -1, 2.5, True, "5"):
            with self.assertRaises(ValueError):
                self.create(users=users)
        self.assertEqual(self.tickets, [])

    def test_unassigned_cannot_start(self):
        t = self.create()
        before = t.copy()
        with self.assertRaises(ValueError):
            change_status(self.tickets, t["id"], "in_progress")
        self.assertEqual(t, before)

    def test_resolved_cannot_be_assigned(self):
        t = self.create()
        assign_ticket(self.tickets, t["id"], "Engineer A")
        change_status(self.tickets, t["id"], "resolved")
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, t["id"], "Engineer B")
        self.assertEqual(t["assigned_to"], "Engineer A")

    def test_notes(self):
        t = self.create()
        n = add_note(self.tickets, t["id"], "Engineer A", "Router checked")
        self.assertEqual(n["note_id"], "N001")
        with self.assertRaises(ValueError):
            add_note(self.tickets, t["id"], "Engineer A", "No")

    def test_resolved_note_rejected(self):
        t = self.create()
        change_status(self.tickets, t["id"], "resolved")
        with self.assertRaises(ValueError):
            add_note(self.tickets, t["id"], "Engineer A", "Router checked")

    def test_queue(self):
        t1 = self.create()
        t2 = self.create("Laptop issue", "low", 1)
        assign_ticket(self.tickets, t1["id"], "Engineer A")
        change_status(self.tickets, t1["id"], "in_progress")
        self.assertEqual(
            [t["id"] for t in open_work_queue(self.tickets)],
            [t2["id"]]
        )

    def test_ticket_ids_are_unique(self):
        t1 = self.create("Wi-Fi issue")
        t2 = self.create("Laptop issue")
        self.assertNotEqual(t1["id"], t2["id"])

    def test_ticket_search(self):
        self.create("Wi-Fi issue")
        self.create("Laptop issue")
        results = search_tickets(self.tickets, "Wi-Fi")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Wi-Fi issue")


    def test_search_returns_empty_for_no_matches(self):
        self.create("Wi-Fi issue")
        results = search_tickets(self.tickets, "printer")
        self.assertEqual(results, [])


    def test_search_is_case_insensitive(self):
        self.create("Wi-Fi issue")
        results = search_tickets(self.tickets, "wI-fI")
        self.assertEqual(len(results), 1)

    def test_search_by_category(self):
        self.create("Wi-Fi issue")
        results = search_tickets(self.tickets, "Network")
        self.assertEqual(len(results), 1)

    def test_search_by_status(self):
        self.create("Wi-Fi issue")
        results = search_tickets(self.tickets, "open")
        self.assertEqual(len(results), 1)

    def test_search_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, "")


if __name__ == "__main__":
    unittest.main()
