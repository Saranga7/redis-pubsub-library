# publisher.py
from library import LibraryDatabase
import time
from datetime import datetime

def add_books(library):
    #Populate database
    library.add_book( isbn = "1001",
                      title = "The Catcher in the Rye", 
                      author = "J.D. Salinger", 
                      copies = 5, 
                      description = "Classic novel about teenage angst", 
                      expiry_days = 14, 
                      language = "English", 
                      year = 1951)
    
    library.add_book("1002", 
                    "To Kill a Mockingbird", 
                    "Harper Lee", 
                    3, 
                    "Classic novel about racial injustice", 
                    expiry_days = 14, language = "English", year = 1960, edition = "1st")
    
    library.add_book("1003", 
                     "The Hobbit", 
                     "J.R.R Tolien", 
                     7, 
                     "Classic fantasy and adventure novel having mystical elements; prequel to LOTR", 
                     expiry_days = 14, language = "English", year = 1937, edition = "3rd")
    
    library.add_book("1004", 
                     "Harry Potter and the Philosopher's Stone", 
                     "J.K. Rowling", 
                     9, 
                     "Adventure, magical, fantasy, novel with mystical elements; first part of the Harry Potter series", 
                     expiry_days = 14, language = "English")

    library.add_book("1005", 
                     "The Invisible Man", 
                     "H.G. Wells", 
                     3, 
                     "Classic scifi novel", 
                     expiry_days = 7, language = "English")
    
    library.add_book("1006",
                     "Deep Learning",
                     "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
                     5,
                     "Reference book for AI and machine learning")
    

def list_all_books(library):
    #Lists all the books present in the database
    all_books = library.list_books()
    main_keys = ['isbn', 'title', 'author', 'expiry_date', 'description']

    print("\n\nBooks in the database:\n")
    for book in all_books:
        for key in main_keys:
            value = book.get(key, '')
            print(f"{key}: {value}")
        for key, value in book.items():
            if key not in main_keys: # since the keys for each book may be different 
                print(f"{key}: {value}")
        print()




def main():
    library = LibraryDatabase() 

    #initialize, remove all books if present already
    library.remove_all_books() 

    # Add books to the database with different expiry dates
    add_books(library)

    # List books in the database
    list_all_books(library)

    # Borrow books and refresh their expiry dates
    isbn_to_borrow_list = ["1001", "1002"]
    for isbn_to_borrow in isbn_to_borrow_list:
        library.borrow_book(isbn_to_borrow)

    # Return a book
    isbn_to_return = "1001"
    library.return_book(isbn_to_return)


    # Sleep for a while to simulate a book expiry
    print("\n\nSimulating days delay in seconds. Please wait...")
    time.sleep(10)


    # Check expiry dates
    print("\n\nChecking expiry status of the books...")
    fake_current_date = datetime(2023, 12, 20).date() # To show the expiry of a book
    library.check_and_expire_books(fake_current_date)


    # List all books in the database after all the operations
    list_all_books(library)

if __name__ == "__main__":
    main()
