# Architectures for Big Data (TPT-DATAAI921) Lab 1

### Assignment
With the help of a programming language interface to Redis, write a toy application of a database of books that can be borrowed in a library. You can use any supported language among the ones listed at https://redis.io/docs/connect/clients/.

#### Application specification

1. All books in the library database have an ISBN, a title, an author and a number of copies.
2. Books may also have other properties, e.g., language, publication year, edition... (up to you).
3. Create a publish-subscribe news system (see https://redis.io/docs/interact/pubsub/) that:
- on the publisher side lets the user add a book to the library, indexes it by the keywords in its description, publishes a channel for each indexed keyword, and emits a news message containing the newly published book ID;
- on the subscriber side enables the user to subscribe to news channels matching certain key- words, retrieve a book from a news by the ID, and show the full book entry from the database; separately the user can borrow or return a book: the system needs to check if the book is available;
- makes books expire after a while (if no one borrows the book): these are no longer available to borrow;
- if someone borrows a book (by, e.g., setting a certain field in the database), makes the book refresh its expiry date.