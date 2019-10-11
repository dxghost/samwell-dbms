# TODO implement different queries
import json
from settings import BOOKS_DATABASE_PATH
from validators import validate_isbn, validate_name, validate_author, validate_publisher, validate_subject, validate_publish_year, validate_pages_count


class Book:
    def __init__(self, ISBN, name, author, publisher, subject, published_year, pages_count):
        # TODO support multi value for authors and subjects
        # ISBN
        validate_isbn(ISBN)
        self.isbn = ISBN
        # NAME
        validate_name(name)
        self.name = name
        # AUTHOR
        validate_author(author)
        self.author = author
        # PUBLISHER
        validate_publisher(publisher)
        self.publisher = publisher
        # SUBJECT
        validate_subject(subject)
        self.subject = subject
        # PUBLISHED YEAR
        validate_publish_year(published_year)
        self.published_year = published_year
        # PAGES COUNT
        validate_pages_count(pages_count)
        self.pages_count = pages_count

    def as_dictionary(self):
        return({
            "ISBN": self.isbn,
            "Name": self.name,
            "Author": self.author,
            "Publisher": self.publisher,
            "Subject": self.subject,
            "PublishYear": self.published_year,
            "PagesCount": self.pages_count
        })

    def __str__(self):
        print("")
        print("Book Name:              %s" % (self.name))
        print("Book ISBN:              %s" % (self.isbn))
        print("Book Author:            %s" % (self.author))
        print("Book Publisher:         %s" % (self.publisher))
        print("Book Subject:           %s" % (self.subject))
        print("Book Published Year:    %s" % (self.published_year))
        print("Book Pages Count:       %s" % (self.pages_count))
        return ""


class Shelf:
    def __init__(self, datas_path):
        self.books = []
        self.books_data = []
        with open(BOOKS_DATABASE_PATH, 'r') as books_database:
            self.books_data = json.load(books_database)
            id_counter = 1
            for book in self.books_data:
                self.books.append(Book(ISBN=book["ISBN"],
                                       name=book["Name"],
                                       author=book["Author"],
                                       publisher=book["Publisher"],
                                       subject=book["Subject"],
                                       published_year=book["PublishYear"],
                                       pages_count=book["PagesCount"]))
                id_counter += 1
                # TODO sync indexers

    def remove_book(self, id):
        print("The book you ordered to remove:")
        print(self.books[id-1])
        del self.books[id-1]
        del self.books_data[id-1]
        self.sync_database()
        # TODO sync indexers

    def edit_book(self, id=None, isbn=None, name=None, author=None,
                  publisher=None, subject=None, published_year=None,
                  pages_count=None):
        if id:
            book = self.books[id-1]
        else:
            raise ValueError(
                "Didn't specify if of the book which needs to be edited.")
        print("Book you ordered to Edit:(befor edition)")
        print(book)
        if isbn:
            validate_isbn(isbn)
            book.isbn = isbn
        if name:
            validate_name(name)
            book.name = name
        if author:
            validate_author(author)
            book.author = author
        if publisher:
            validate_publisher(publisher)
            book.publisher = publisher
        if subject:
            validate_subject(subject)
            book.subject = subject
        if published_year:
            validate_publish_year(published_year)
            book.published_year = published_year
        if pages_count:
            validate_pages_count(pages_count)
            book.pages_count = pages_count
        print("The current status of book:(after edition)")
        print(book)
        self.books_data[id-1] = self.books[id-1].as_dictionary()
        self.sync_database()

    def sync_database(self):
        print("Saving Changes to disk.")
        with open(BOOKS_DATABASE_PATH, 'w') as books_database:
            json.dump(self.books_data, books_database)
        print("Changes saved to disk successfully.")

    def add_book(self, book):
        if(type(book) != Book):
            raise TypeError(
                "Only book instances are allowed, given %s." % (type(book)))
        print(book)
        print("Adding to Shelf.")
        self.books.append(book)
        self.books_data.append(book.as_dictionary())
        print("Saving added book to disk.")
        self.sync_database()
        # TODO sync indexers

    def __str__(self):
        print("The books available in shelf:")
        for book in self.books:
            print(book)
        return ""


if __name__ == "__main__":
    s = Shelf(BOOKS_DATABASE_PATH)
    b = Book(96521113921231300000,
             "DEJAVU's Story",
             "Mahdi DuXi",
             "Ghostu Academy",
             "Bio",
             2022,
             9101)
    # s.add_book(b)
    s.edit_book(id=4, isbn=99521113921231300000)
    # s.remove_book(2)
    print()
    print(s)
