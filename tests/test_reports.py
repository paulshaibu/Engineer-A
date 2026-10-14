import unittest
from campusflow.tickets import create_ticket, assign_ticket
from campusflow.reports import generate_report


class TestReports(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi problem", "Network", "high", 10)
        create_ticket(self.tickets, "Laptop problem", "Hardware", "low", 1)

    def test_total_tickets(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["total_tickets"], 2)

    def test_status_counts(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["by_status"]["open"], 2)

    def test_assigned_and_unassigned_counts(self):
        assign_ticket(self.tickets, 1, "Engineer A")
        report = generate_report(self.tickets)
        self.assertEqual(report["assigned"], 1)
        self.assertEqual(report["unassigned"], 1)

    def test_empty_report(self):
        report = generate_report([])
        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["assigned"], 0)
        self.assertEqual(report["unassigned"], 0)


if __name__ == "__main__":
    unittest.main()
