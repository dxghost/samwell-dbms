# TODO implement different queries
# TODO implement unique=True for ISBN
import json
from settings import BOOKS_DATABASE_PATH, BOOK_AUTHOR_INDEX, BOOK_ISBN_INDEX, BOOK_NAME_INDEX
from validators import validate_isbn, validate_name, validate_author, validate_publisher, validate_subject, validate_publish_year, validate_pages_count
from id_gen import get_book_id


class Book:
    def __init__(self, ISBN, name, author, publisher, subject, published_year, pages_count, id=None):
        # TODO support multi value for authors and subjects
        self.id = id
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
            "ID": self.id,
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
        print("Book ID:                %s" % (self.id))
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
        self.books = {}
        self.books_data = {}
        self.books_author_data = {}
        self.books_isbn_data = {}
        self.books_name_data = {}
        with open(BOOKS_DATABASE_PATH, 'r') as books_database:
            self.books_data = json.load(books_database)
            for book in self.books_data:
                book = self.books_data[book]
                author = book["Author"]
                isbn = book["ISBN"]
                name = book["Name"]
                id = book["ID"]
                self.books[id] = Book(ISBN=isbn,
                                      name=name,
                                      author=author,
                                      publisher=book["Publisher"],
                                      subject=book["Subject"],
                                      published_year=book["PublishYear"],
                                      pages_count=book["PagesCount"],
                                      id=book["ID"])
                # if book["Author"] in self.books_author_data:
                #     self.books_author_data[author].append(id)
                # else:
                #     self.books_author_data[author] = [id]

                # if book["Name"] in self.books_name_data:
                #     self.books_name_data[name].append(id)
                # else:
                #     self.books_name_data[name] = [id]

                # self.books_isbn_data[isbn] = id

        with open(BOOK_AUTHOR_INDEX, 'r') as author_index_table:
            self.books_author_data = json.load(author_index_table)
        with open(BOOK_ISBN_INDEX, 'r') as isbn_index_table:
            self.books_isbn_data = json.load(isbn_index_table)
        with open(BOOK_NAME_INDEX, 'r') as name_index_table:
            self.books_name_data = json.load(name_index_table)



        # self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)
        # self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)
        # self.sync_database(BOOK_NAME_INDEX, self.books_name_data)

    def remove_book(self, id):
        print("The book you ordered to remove:")
        book = self.books[id]
        print(book)
        self.books_author_data[book.author].remove(book.id)
        self.books_name_data[book.name].remove(book.id)
        del self.books_isbn_data[str(book.isbn)]
        del self.books[id]
        del self.books_data[str(id)]
        self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
        self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)
        self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)
        self.sync_database(BOOK_NAME_INDEX, self.books_name_data)

    def edit_book(self, id=None, isbn=None, name=None, author=None,
                  publisher=None, subject=None, published_year=None,
                  pages_count=None):
        if id:
            book = self.books[id]
        else:
            raise ValueError(
                "Didn't specify if of the book which needs to be edited.")
        print("Book you ordered to Edit:(befor edition)")
        print(book)

        if isbn:
            validate_isbn(isbn)
            self.books_isbn_data[str(isbn)] = self.books_isbn_data[str(book.isbn)]
            del self.books_isbn_data[str(book.isbn)]
            book.isbn = isbn
            self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)

        if name:
            validate_name(name)
            if name in self.books_name_data:
                self.books_name_data[name].append(book.id)
            else:
                self.books_name_data[name] = [book.id]
            self.books_name_data[book.name].remove(book.id)
            book.name = name
            self.sync_database(BOOK_NAME_INDEX, self.books_name_data)

        if author:
            validate_author(author)
            if author in self.books_author_data:
                self.books_author_data[author].append(book.id)
            else:
                self.books_author_data[author] = [book.id]
            self.books_author_data[book.author].remove(book.id)
            book.author = author
            self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)

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
        print((self.books_data.keys()))
        self.books_data[str(id)] = self.books[id].as_dictionary()
        self.sync_database(BOOKS_DATABASE_PATH, self.books_data)

    def sync_database(self, file_path, data):
        print("Saving Changes to %s." % (file_path))
        with open(file_path, 'w') as database:
            json.dump(data, database)
        print("Changes saved to disk successfully.")

    def add_book(self, book):
        if(type(book) != Book):
            raise TypeError(
                "Only book instances are allowed, given %s." % (type(book)))

        print("Adding to Shelf.")
        id = get_book_id()
        book.id = id
        print(book)
        self.books[id] = book
        self.books_data[id] = book.as_dictionary()

        if book.author in self.books_author_data:
            self.books_author_data[book.author].append(book.id)
        else:
            self.books_author_data[book.author] = [book.id]

        if book.name in self.books_name_data:
            self.books_name_data[book.name].append(book.id)
        else:
            self.books_name_data[book.name] = [book.id]

        self.books_isbn_data[book.isbn] = book.id
        print("Saving added book to disk.")
        self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
        self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)
        self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)
        self.sync_database(BOOK_NAME_INDEX, self.books_name_data)

    def __str__(self):
        print("The books available in shelf:")
        for book in self.books:
            print(self.books[book])
        return ""


if __name__ == "__main__":
    s = Shelf(BOOKS_DATABASE_PATH)
    b = Book(43521113921231300000,
             "Army of the living",
             "Elaria Sand",
             "dasda Academy",
             "adsasd",
             2022,
             29)
    # s.add_book(b)
    # s.edit_book(id=3, isbn=80021113921231300000,author="Wu Zi",name="Army of chinese")
    s.remove_book(2)
    print()
    print(s)
