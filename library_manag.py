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
                    if len(parts) == 6:
                        self.books.append({
                            "id": parts[0],
                            "title": parts[1],
                            "author": parts[2],
                            "status": parts[3].lower(),
                            "borrower": parts[4],
                            "issued_date": parts[5]
                        })
                    elif len(parts) == 5:
                        self.books.append({
                            "id": parts[0],
                            "title": parts[1],
                            "author": parts[2],
                            "status": parts[3].lower(),
                            "borrower": parts[4],
                            "issued_date": ""
                        })

    def save_books(self):
        with open(self.filename, "w") as f:
            for b in self.books:
                f.write(f"{b['id']}|{b['title']}|{b['author']}|{b['status']}|{b['borrower']}|{b['issued_date']}\n")

    def show_books(self):
        available = [b for b in self.books if b["status"] == "available"]
        if not available:
            print("\n📕 No books available.\n")
            return
        headers = ["ID", "Title", "Author"]
        rows = [[b["id"], b["title"], b["author"]] for b in available]
        print("\n📚 Available Books:")
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

    def add_book(self):
        bid = input("Enter Book ID: ")
        title = input("Enter Book Title: ")
        author = input("Enter Author: ")
        self.books.append({
            "id": bid, "title": title, "author": author,
            "status": "available", "borrower": "", "issued_date": ""
        })
        self.save_books()
        print("✅ Book added.")

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
                return
        print("❌ Book not found or already issued.")

    def return_book(self):
        bid = input("Enter Book ID to return: ")
        for b in self.books:
            if b["id"] == bid and b["status"] == "issued":
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
        else:
            print("❌ Book ID not found.")

def main():
    lib = Library()
    print("📖 Welcome to the Library Management System")
    while True:
        print("\n📚 LIBRARY MENU")
        print("1. Show available books")
        print("2. Show issued books")
        print("3. Add new book")
        print("4. Issue book")
        print("5. Return book")
        print("6. Remove book")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            lib.show_books()
        elif choice == "2":
            lib.show_issued_books()
        elif choice == "3":
            lib.add_book()
        elif choice == "4":
            lib.issue_book()
        elif choice == "5":
            lib.return_book()
        elif choice == "6":
            lib.remove_book()
        elif choice == "7":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
