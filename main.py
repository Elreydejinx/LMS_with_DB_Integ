# main.py
from user_interactions import add_book, borrow_book, return_book, search_book, display_books
from error_handling import handle_db_error, handle_input_error

def display_main_menu():
    print("Welcome to the Library Management System!")
    print("Main Menu:")
    print("1. Book Operations")
    print("2. User Operations")
    print("3. Author Operations")
    print("4. Quit")

def display_book_menu():
    print("Book Operations:")
    print("1. Add a new book")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Search for a book")
    print("5. Display all books")

def main():
    while True:
        display_main_menu()
        choice = input("Select an option: ")

        if choice == '1':
            while True:
                display_book_menu()
                book_choice = input("Select an option: ")

                if book_choice == '1':
                    try:
                        add_book()
                    except Exception as e:
                        handle_db_error(e)
                elif book_choice == '2':
                    try:
                        borrow_book()
                    except Exception as e:
                        handle_db_error(e)
                elif book_choice == '3':
                    try:
                        return_book()
                    except Exception as e:
                        handle_db_error(e)
                elif book_choice == '4':
                    try:
                        search_book()
                    except Exception as e:
                        handle_db_error(e)
                elif book_choice == '5':
                    try:
                        display_books()
                    except Exception as e:
                        handle_db_error(e)
                else:
                    print("Invalid option. Returning to main menu.")
                break

        elif choice == '2':
            print("User Operations feature is not implemented yet.")

        elif choice == '3':
            print("Author Operations feature is not implemented yet.")

        elif choice == '4':
            print("Quitting the application.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
