# user_interactions.py
import re
from db_operations import execute_query, fetch_query

def validate_input(prompt, regex):
    """Validate user input using regex."""
    while True:
        value = input(prompt)
        if re.match(regex, value):
            return value
        else:
            print("Invalid input. Please try again.")

def add_book():
    """Add a new book to the database."""
    title = input("Enter book title: ")
    author_name = input("Enter author name: ")
    genre = input("Enter genre: ")
    pub_date = validate_input("Enter publication date (YYYY-MM-DD): ", r"\d{4}-\d{2}-\d{2}")
    
    # Get author ID or insert new author
    author_query = "SELECT id FROM authors WHERE name = %s"
    author_id = fetch_query(author_query, (author_name,))
    if author_id:
        author_id = author_id[0][0]
    else:
        author_query = "INSERT INTO authors (name) VALUES (%s)"
        execute_query(author_query, (author_name,))
        author_id = fetch_query("SELECT LAST_INSERT_ID()")[0][0]
    
    book_query = "INSERT INTO books (title, author_id, genre, pub_date) VALUES (%s, %s, %s, %s)"
    execute_query(book_query, (title, author_id, genre, pub_date))
    print("Book added successfully!")

def borrow_book():
    """Allow a user to borrow a book."""
    user_id = validate_input("Enter your user ID: ", r"^[\w-]+$")
    book_title = input("Enter book title to borrow: ")
    
    # Get book ID
    book_query = "SELECT id, availability FROM books WHERE title = %s"
    book = fetch_query(book_query, (book_title,))
    if book:
        book_id, availability = book[0]
        if not availability:
            print("Book is already borrowed.")
            return
        # Check user existence
        user_query = "SELECT id FROM users WHERE user_id = %s"
        user = fetch_query(user_query, (user_id,))
        if not user:
            print("User not found.")
            return
        
        user_id = user[0][0]
        due_date = input("Enter due date (YYYY-MM-DD): ")
        borrow_query = "INSERT INTO borrowed_books (book_id, user_id, borrowed_date, due_date) VALUES (%s, %s, CURDATE(), %s)"
        execute_query(borrow_query, (book_id, user_id, due_date))
        execute_query("UPDATE books SET availability = FALSE WHERE id = %s", (book_id,))
        print("Book borrowed successfully!")
    else:
        print("Book not found.")

def return_book():
    """Allow a user to return a book."""
    user_id = validate_input("Enter your user ID: ", r"^[\w-]+$")
    book_title = input("Enter book title to return: ")
    
    book_query = "SELECT id FROM books WHERE title = %s"
    book = fetch_query(book_query, (book_title,))
    if book:
        book_id = book[0][0]
        return_query = "UPDATE books SET availability = TRUE WHERE id = %s"
        execute_query(return_query, (book_id,))
        
        # Find borrowed book record
        borrow_query = "SELECT id FROM borrowed_books WHERE book_id = %s AND user_id = %s AND returned = FALSE"
        borrowed = fetch_query(borrow_query, (book_id, user_id))
        if borrowed:
            borrow_id = borrowed[0][0]
            execute_query("UPDATE borrowed_books SET returned = TRUE WHERE id = %s", (borrow_id,))
            print("Book returned successfully!")
        else:
            print("No record of this book being borrowed by you.")
    else:
        print("Book not found.")

def search_book():
    """Search for a book by title."""
    title = input("Enter book title to search: ")
    query = "SELECT books.title, authors.name, books.genre, books.pub_date, books.availability FROM books JOIN authors ON books.author_id = authors.id WHERE books.title = %s"
    results = fetch_query(query, (title,))
    if results:
        for result in results:
            print(f"Title: {result[0]}, Author: {result[1]}, Genre: {result[2]}, Publication Date: {result[3]}, Available: {result[4]}")
    else:
        print("Book not found.")

def display_books():
    """Display all books in the database."""
    query = "SELECT books.title, authors.name, books.genre, books.pub_date, books.availability FROM books JOIN authors ON books.author_id = authors.id"
    results = fetch_query(query)
    if results:
        for result in results:
            print(f"Title: {result[0]}, Author: {result[1]}, Genre: {result[2]}, Publication Date: {result[3]}, Available: {result[4]}")
    else:
        print("No books available.")
