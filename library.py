# library.py
import redis
import string
from datetime import datetime, timedelta


class LibraryDatabase:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port = 6379, decode_responses=True) # Connect to Redis
        self.redis_client.flushdb() # Flush entire database
        self.remove_puntuations = str.maketrans("", "", string.punctuation) # to remove punctuations

    def add_book(self, isbn, title, author, copies, description, expiry_days = 7, **kwargs):
        book_key = f"book:{isbn}"
        expiry_date = (datetime.utcnow() + timedelta(days = expiry_days)).date()  # date() for only the date portion
        book_data = {
            'isbn': isbn,
            'title': title,
            'author': author,
            'copies': copies,
            'description': description,
            'expiry_days': expiry_days,  # Set initial expiry days
            'expiry_date': expiry_date.isoformat()
        }
        book_data.update(kwargs)
        self.redis_client.hmset(book_key, book_data)

        cleaned_description = description.translate(self.remove_puntuations) #remove punctuation marks in description
        keywords = set(cleaned_description.lower().split())
        for keyword in keywords:
            self.redis_client.sadd(f"keyword:{keyword}", isbn)

        news_message = f"New book published: {title} by {author}, ISBN: {isbn}"
        self.redis_client.publish("news", news_message)

    def get_book(self, isbn):
        book_key = f"book:{isbn}"
        return self.redis_client.hgetall(book_key)

    def borrow_book(self, isbn, num_borrowed = 1):
        book_key = f"book:{isbn}"
        book_name = self.redis_client.hget(book_key, 'title')
        current_copies = int(self.redis_client.hget(book_key, 'copies'))
        if current_copies >= num_borrowed:
            self.redis_client.hset(book_key, 'copies', current_copies - num_borrowed)
            self._refresh_expiry_date(book_key)  # Refresh expiry date when a book is borrowed
            news_message = f"{book_name}  (ISBN : {isbn}) has been borrowed.\n\tNumber of copies available now: {current_copies - num_borrowed}"
            self.redis_client.publish("news", news_message)
            print("\n" + news_message)
        else:
            news_message = f"There are no available copies of the book with ISBN {isbn} at the moment."
            self.redis_client.publish("news", news_message)
            print("\n" + news_message)

    def return_book(self, isbn, num_returned = 1):
        book_key = f"book:{isbn}"
        book_name = self.redis_client.hget(book_key, 'title')
        current_copies = int(self.redis_client.hget(book_key, 'copies'))
        self.redis_client.hset(book_key, 'copies', current_copies + num_returned)
        news_message = f"{book_name} (ISBN : {isbn}) has been returned.\n\tNumber of copies available now: {current_copies + num_returned}"
        self.redis_client.publish("news", news_message)
        print("\n" + news_message)

    def list_books(self):
        book_keys = self.redis_client.keys("book:*")
        books = [self.redis_client.hgetall(key) for key in book_keys]
        return books

    def subscribe_to_channel(self, channel, callback):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message['type'] == 'message':
                callback(message['data'])

    def check_and_expire_books(self, simulated_current_date = None):
        # Check expiry status of the books. If expired, remove book
        book_keys = self.redis_client.keys("book:*")
        if simulated_current_date:
            current_date = simulated_current_date
        else:
            current_date = datetime.utcnow().date()

        for book_key in book_keys:
            book_data = self.redis_client.hgetall(book_key)

            expiry_date_str = book_data.get('expiry_date')
            if expiry_date_str:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()

                if current_date >= expiry_date:
                    # If book has reached expiry date, remove it
                    self.redis_client.delete(book_key)
                    news_message = f"{book_data['title']}  (ISBN: {book_data['isbn']}) has expired. Hence, removing from database."
                    print(news_message)
                    self.redis_client.publish("news", news_message)


    def remove_book(self, isbn):
        # remove a particular book according to isbn
        book_key = f"book:{isbn}"
        self.redis_client.delete(book_key)

    def remove_all_books(self):
        # remove all books in the database
        book_keys = self.redis_client.keys("book:*")
        for book_key in book_keys:
            self.redis_client.delete(book_key)

    def _refresh_expiry_date(self, book_key):
        # Refresh the expiry date when a book is borrowed
        expiry_days = int(self.redis_client.hget(book_key, 'expiry_days'))
        new_expiry_date = (datetime.utcnow() + timedelta(days = expiry_days)).date().isoformat()
        self.redis_client.hset(book_key, 'expiry_date', new_expiry_date)
