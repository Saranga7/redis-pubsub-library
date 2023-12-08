from library import LibraryDatabase

def news_callback(message):
    # Callback function to handle news messages
    print(f"News: {message}")


def main():
    # Create an instance of the LibraryDatabase class for subscribing
    subscriber = LibraryDatabase()

    # Subscribe to the "news" channel and provide the news_callback function as the callback
    subscriber.subscribe_to_channel("news", news_callback)

if __name__ == "__main__":
    main()
