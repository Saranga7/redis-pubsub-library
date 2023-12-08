import sys
import redis
from publisher import add_books
from library import LibraryDatabase


def retrieve_books_by_keyword(redis_client, keyword):
    # Retrieve all books (ISBNs) associated with the keyword
    related_books = redis_client.smembers(f"keyword:{keyword}")

    print(f"\nRetrieving books according to keyword:{keyword}\n\n")
    # Display information for each book
    for isbn in related_books:
        book_info = redis_client.hgetall(f"book:{isbn}")
        print(f"Book: {book_info.get('title')}\nAuthor: {book_info.get('author')}\nISBN: {isbn}", end = "\n\n")

def main():
    # Connect to Redis
    redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
    # Clear database
    redis_client.flushdb()

    # Populate database
    library = LibraryDatabase() 
    add_books(library) 

    # Check if a keyword is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Error! Required keyword.\nUsage: python script.py <keyword>")
        sys.exit(1)

    keyword = sys.argv[1]

    # Retrieve and display books related to the keyword
    retrieve_books_by_keyword(redis_client, keyword)




if __name__ == "__main__":
    main()
