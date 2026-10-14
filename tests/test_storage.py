import json
import os
import tempfile
import unittest

from campusflow.tickets import create_ticket, add_note
from campusflow.storage import save_tickets, load_tickets


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "tickets.json")
        self.tickets = []
        t = create_ticket(self.tickets, "Wi-Fi issue", "Network", "high", 10)
        add_note(self.tickets, t["id"], "Engineer A", "Router checked")

    def tearDown(self):
        self.folder.cleanup()

    def test_save_load(self):
        save_tickets(self.path, self.tickets)
        self.assertEqual(load_tickets(self.path), self.tickets)

    def test_corrupt_json(self):
        with open(self.path, "w") as f:
            f.write("{bad")
        with self.assertRaises(json.JSONDecodeError):
            load_tickets(self.path)

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            save_tickets(self.path, [self.tickets[0], self.tickets[0]])

    def test_next_ticket_id(self):
        save_tickets(self.path, self.tickets)
        tickets = load_tickets(self.path)
        t = create_ticket(tickets, "Laptop issue", "Hardware", "low", 1)
        self.assertEqual(t["id"], 2)

    def test_next_note_id(self):
        save_tickets(self.path, self.tickets)
        tickets = load_tickets(self.path)
        n = add_note(tickets, 1, "Engineer B", "Switch checked")
        self.assertEqual(n["note_id"], "N002")


if __name__ == "__main__":
    unittest.main()