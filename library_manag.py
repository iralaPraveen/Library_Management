import os
from datetime import datetime
from tabulate import tabulate

class Library:
    def __init__(self, filename="library.txt"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        self.books.clear()
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) >= 3:
                        self.books.append({
                            "id": parts[0],
                            "title": parts[1],
                            "author": parts[2],
                            "status": "available",
                            "borrower": "",
                            "issued_date": ""
                        })

    def save_books(self):
        with open(self.filename, "w") as f:
            for b in self.books:
                f.write(f"{b['id']}|{b['title']}|{b['author']}|{b['status']}|{b['borrower']}|{b['issued_date']}\n")

    def log_activity(self, message):
        with open("log.txt", "a") as log:
            log.write(f"{datetime.now()} - {message}\n")

    def is_unique_id(self, bid):
        return all(b["id"] != bid for b in self.books)

    def show_books(self):
        available = [b for b in self.books if b["status"] == "available"]
        if not available:
            print("\n📕 No books available.\n")
            return
        headers = ["ID", "Title", "Author"]
        rows = [[b["id"], b["title"], b["author"]] for b in available]
        print("\n📚 Available Books:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def show_all_books(self):
        if not self.books:
            print("\n📘 No books in library.\n")
            return
        headers = ["ID", "Title", "Author", "Status"]
        rows = [[b["id"], b["title"], b["author"], b["status"]] for b in self.books]
        print("\n📚 All Books:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def show_issued_books(self):
        issued = [b for b in self.books if b["status"] == "issued"]
        if not issued:
            print("\n📙 No books issued.\n")
            return
        headers = ["ID", "Title", "Author", "Borrower", "Issued On"]
        rows = [[b["id"], b["title"], b["author"], b["borrower"], b["issued_date"]] for b in issued]
        print("\n📕 Issued Books:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def check_overdue_books(self):
        overdue = []
        for b in self.books:
            if b["status"] == "issued" and b["issued_date"]:
                issued_date = datetime.strptime(b["issued_date"], '%Y-%m-%d %H:%M:%S')
                if (datetime.now() - issued_date).days > 7:
                    overdue.append(b)
        if overdue:
            headers = ["ID", "Title", "Borrower", "Issued Date"]
            rows = [[b["id"], b["title"], b["borrower"], b["issued_date"]] for b in overdue]
            print("\n🔔 Overdue Books:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("\n✅ No overdue books.")

    def add_book(self):
        bid = input("Enter Book ID: ")
        if not self.is_unique_id(bid):
            print("❌ Book ID already exists.")
            return
        title = input("Enter Book Title: ")
        author = input("Enter Author: ")
        self.books.append({
            "id": bid, "title": title, "author": author,
            "status": "available", "borrower": "", "issued_date": ""
        })
        self.save_books()
        print("✅ Book added.")
        self.log_activity(f"Book '{title}' (ID: {bid}) added.")

    def issue_book(self):
        bid = input("Enter Book ID to issue: ")
        for b in self.books:
            if b["id"] == bid and b["status"] == "available":
                name = input("Enter Borrower Name: ")
                b["status"] = "issued"
                b["borrower"] = name
                b["issued_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_books()
                print("✅ Book issued.")
                self.log_activity(f"Book '{b['title']}' (ID: {bid}) issued to {name}.")
                return
        print("❌ Book not found or already issued.")

    def return_book(self):
        bid = input("Enter Book ID to return: ")
        for b in self.books:
            if b["id"] == bid and b["status"] == "issued":
                self.log_activity(f"Book '{b['title']}' (ID: {bid}) returned by {b['borrower']}.")
                b["status"] = "available"
                b["borrower"] = ""
                b["issued_date"] = ""
                self.save_books()
                print("✅ Book returned.")
                return
        print("❌ Book not found or not issued.")

    def remove_book(self):
        bid = input("Enter Book ID to remove: ")
        before = len(self.books)
        self.books = [b for b in self.books if b["id"] != bid]
        self.save_books()
        if len(self.books) < before:
            print("✅ Book removed.")
            self.log_activity(f"Book (ID: {bid}) removed.")
        else:
            print("❌ Book ID not found.")

    def search_book(self):
        query = input("Enter title, author, or ID to search: ").lower()
        results = [b for b in self.books if query in b["id"].lower() or query in b["title"].lower() or query in b["author"].lower()]
        if results:
            headers = ["ID", "Title", "Author", "Status"]
            rows = [[b["id"], b["title"], b["author"], b["status"]] for b in results]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("❌ No matching books found.")

def main():
    lib = Library()
    print("📖 Welcome to the Library Management System")
    while True:
        print("\n📚 LIBRARY MENU")
        print("1. Show all books")
        print("2. Show issued books")
        print("3. Show status of all books")
        print("4. Add new book")
        print("5. Issue book")
        print("6. Return book")
        print("7. Remove book")
        print("8. Search for a book")
        print("9. Check overdue books")
        print("10. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            lib.show_books()
        elif choice == "2":
            lib.show_issued_books()
        elif choice == "3":
            lib.show_all_books()
        elif choice == "4":
            lib.add_book()
        elif choice == "5":
            lib.issue_book()
        elif choice == "6":
            lib.return_book()
        elif choice == "7":
            lib.remove_book()
        elif choice == "8":
            lib.search_book()
        elif choice == "9":
            lib.check_overdue_books()
        elif choice == "10":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
