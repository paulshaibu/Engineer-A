from campusflow.tickets import (
    create_ticket,
    search_tickets,
    assign_ticket,
    change_status,
    add_note,
    view_notes,
    open_work_queue,
)
from campusflow.storage import save_tickets, load_tickets
from campusflow.reports import generate_report

FILE = "tickets.json"


def main():
    try:
        tickets = load_tickets(FILE)
    except (FileNotFoundError, ValueError):
        tickets = []

    while True:
        print("\n=== CampusFlow ===")
        print("1. Create ticket")
        print("2. View all tickets")
        print("3. Search tickets")
        print("4. Assign ticket")
        print("5. Change ticket status")
        print("6. Add follow-up note")
        print("7. View ticket notes")
        print("8. View open work queue")
        print("9. Generate report")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Ticket title: ")
                category = input("Category (Network, Hardware, Software, Other): ")
                urgency = input("Urgency (low, medium, high): ")
                users = int(input("Number of affected users: "))

                ticket = create_ticket(tickets, title, category, urgency, users)
                save_tickets(FILE, tickets)
                print("Ticket created:", ticket)

            elif choice == "2":
                for ticket in tickets:
                    print(ticket)

            elif choice == "3":
                query = input("Search by title, category, or status: ")
                results = search_tickets(tickets, query)
                for ticket in results:
                    print(ticket)
                if not results:
                    print("No matching tickets found.")

            elif choice == "4":
                ticket_id = int(input("Ticket ID: "))
                staff = input("Staff name: ")
                assign_ticket(tickets, ticket_id, staff)
                save_tickets(FILE, tickets)
                print("Ticket assigned.")

            elif choice == "5":
                ticket_id = int(input("Ticket ID: "))
                status = input("New status (open, in_progress, resolved): ")
                change_status(tickets, ticket_id, status)
                save_tickets(FILE, tickets)
                print("Status updated.")

            elif choice == "6":
                ticket_id = int(input("Ticket ID: "))
                author = input("Your name: ")
                message = input("Follow-up note: ")
                add_note(tickets, ticket_id, author, message)
                save_tickets(FILE, tickets)
                print("Note added.")

            elif choice == "7":
                ticket_id = int(input("Ticket ID: "))
                for note in view_notes(tickets, ticket_id):
                    print(note)

            elif choice == "8":
                for ticket in open_work_queue(tickets):
                    print(ticket)

            elif choice == "9":
                print(generate_report(tickets))

            elif choice == "0":
                break

            else:
                print("Invalid option. Try again.")

        except (ValueError, TypeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()