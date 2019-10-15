import json
from core.settings import BOOKS_DATABASE_PATH, BOOK_AUTHOR_INDEX, BOOK_ISBN_INDEX, BOOK_NAME_INDEX
from core.validators import validate_isbn, validate_name, validate_author, validate_publisher, validate_subject, validate_publish_year, validate_pages_count
from core.id_gen import get_book_id


class Book:
    def __init__(self, ISBN, name, author, publisher, subject, published_year, pages_count, id=None, admin=False):
        # TODO support multi value for authors and subjects
        if admin == False:
            validate_isbn(ISBN)
            validate_name(name)
            validate_author(author)
            validate_publisher(publisher)
            validate_subject(subject)
            validate_publish_year(published_year)
            validate_pages_count(pages_count)

        self.id = id
        self.isbn = ISBN
        self.name = name
        self.author = author
        self.publisher = publisher
        self.subject = subject
        self.published_year = published_year
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
        print("Publisher Name: ")
        print("Publisher Field: ")
        print("Publisher Address")
        return ""


class Shelf:
    def __init__(self):
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
                                  id=book["ID"],
                                  admin=True)

        with open(BOOK_AUTHOR_INDEX, 'r') as author_index_table:
            self.books_author_data = json.load(author_index_table)
        with open(BOOK_ISBN_INDEX, 'r') as isbn_index_table:
            self.books_isbn_data = json.load(isbn_index_table)
        with open(BOOK_NAME_INDEX, 'r') as name_index_table:
            self.books_name_data = json.load(name_index_table)

    def set_publishers_ministry(self, ministry):
        self.ministry = ministry
        print("[set_publishers_ministry] Ministry set.")

    def update(self, table):
        if table == "BOOK_AUTHOR":
            self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)
        elif table == "BOOK_ISBN":
            self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)
        elif table == "BOOK_NAME":
            self.sync_database(BOOK_NAME_INDEX, self.books_name_data)
        elif table == "BOOKS":
            self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
        else:
            print("[Book update] Enter Correct table name.")
            print(
                "[Book update] Choices are: BOOK_AUTHOR, BOOK_ISBN, BOOK_NAME, BOOKS.")

    def remove_book(self, id):
        print("[remove_book] The book you ordered to remove:")
        book = self.books[id]
        print(book)
        self.books_author_data[book.author].remove(book.id)
        self.books_name_data[book.name].remove(book.id)
        self.ministry.publishers_data[book.publisher]["Books"].remove(book.id)
        del self.books_isbn_data[str(book.isbn)]
        del self.books[id]
        del self.books_data[str(id)]
        self.update("BOOKS")
        self.update("BOOK_AUTHOR")
        self.update("BOOK_NAME")
        self.update("BOOK_ISBN")
        self.ministry.update("PUBLISHERS")
        print("------------------------------------------------------")

    def edit_book(self, id=None, isbn=None, name=None, author=None,
                  publisher=None, subject=None, published_year=None,
                  pages_count=None):
        if id:
            book = self.books[id]
        else:
            raise ValueError(
                "Didn't specify if of the book which needs to be edited.")
        print("[edit_book] Book you ordered to Edit:(befor edition)")
        print(book)

        if isbn:
            validate_isbn(isbn)
            self.books_isbn_data[str(
                isbn)] = self.books_isbn_data[str(book.isbn)]
            del self.books_isbn_data[str(book.isbn)]
            book.isbn = isbn
            self.update("BOOK_ISBN")

        if name:
            validate_name(name)
            if name in self.books_name_data:
                self.books_name_data[name].append(book.id)
            else:
                self.books_name_data[name] = [book.id]
            self.books_name_data[book.name].remove(book.id)
            book.name = name
            self.update("BOOK_NAME")

        if author:
            validate_author(author)
            if author in self.books_author_data:
                self.books_author_data[author].append(book.id)
            else:
                self.books_author_data[author] = [book.id]
            self.books_author_data[book.author].remove(book.id)
            book.author = author
            self.update("BOOK_AUTHOR")

        if publisher:
            if publisher not in self.ministry.publishers_data:
                print(
                    "[edit_book] Ignored. Theres no publisher with given name. %s" % (publisher))
            validate_publisher(publisher)
            self.ministry.publishers_data[book.publisher]["Books"].remove(
                book.id)
            self.ministry.publishers_data[publisher]["Books"].append(book.id)
            self.ministry.update("PUBLISHERS")
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

        print("[edit_book] The current status of book:(after edition)")
        print(book)
        print((self.books_data.keys()))
        self.books_data[str(id)] = self.books[id].as_dictionary()
        # self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
        self.update("BOOKS")
        print("-------------------------------------")

    def sync_database(self, file_path, data):
        print("[sync_database] Saving Changes to %s." % (file_path))
        with open(file_path, 'w') as database:
            json.dump(data, database)
        print("[sync_database] Changes saved to disk successfully.")
        print("-------------------------------------")

    def add_book(self, book):
        if(type(book) != Book):
            raise TypeError(
                "Only book instances are allowed, given %s." % (type(book)))
        if book.publisher not in self.ministry.publishers_data:
            raise ValueError(
                "Theres no publisher with given name. %s" % (book.publisher))

        print("[add_book] Adding to Shelf.")
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

        self.ministry.publishers_data[book.publisher]["Books"].append(
            book.id)
        self.ministry.update("PUBLISHERS")
        print("self.ministry.publishers[book.publisher].published_books: %s" % (
            self.ministry.publishers[book.publisher].published_books))

        self.books_isbn_data[book.isbn] = book.id
        # self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
        self.update("BOOKS")
        # self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)
        self.update("BOOK_AUTHOR")
        # self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)
        self.update("BOOK_ISBN")
        # self.sync_database(BOOK_NAME_INDEX, self.books_name_data)
        self.update("BOOK_NAME")
        print("------------------------------------------------------")

    def get_by_exact_name(self, book_name):
        books = []
        if book_name in self.books_name_data:
            result = self.books_name_data[book_name]
            for i in result:
                books.append(self.books[i])
        return books

    def get_by_name(self, book_name):
        books = []
        for bk_nm in self.books_name_data.keys():
            if book_name in bk_nm:
                for book_id in self.books_name_data[bk_nm]:
                    books.append(self.books[book_id])
        return books

    def get_by_subject(self, subject):
        books = []
        for book in self.books.values():
            if subject in book.subject:
                books.append(book)
        return books

    def get_by_isbn(self, isbn):
        isbn = str(isbn)
        if isbn in self.books_isbn_data:
            return self.books[self.books_isbn_data[isbn]]
        else:
            return None

    def get_by_author(self, author_name):
        books = []
        if author_name in self.books_author_data:
            for book_id in self.books_author_data[author_name]:
                books.append(self.books[book_id])
        return books

    def show_by_id(self, id):
        if id not in self.books:
            print("[show_by_id] No book found with given id %s." % (id))
            return
        book = self.books[id]
        publisher = self.ministry.publishers[book.publisher]
        print("")
        print("Book ID:                %s" % (book.id))
        print("Book Name:              %s" % (book.name))
        print("Book ISBN:              %s" % (book.isbn))
        print("Book Author:            %s" % (book.author))
        print("Book Subject:           %s" % (book.subject))
        print("Book Published Year:    %s" % (book.published_year))
        print("Book Pages Count:       %s" % (book.pages_count))
        print("Book Publisher:         %s" % (book.publisher))
        print("Publisher Name:         %s" % (publisher.name))
        print("Publisher Number:       %s" % (publisher.number))
        print("Publisher Field:        %s" % (publisher.field))
        print("Publisher Manager:      %s" % (publisher.manager_name))
        print("Publisher Address:      %s" % (publisher.address))
        print("Publisher Books:        %s" % (publisher.published_books))

    def __str__(self):
        print("The books available in shelf:")
        for book in self.books:
            print(self.books[book])
        return ""


if __name__ == "__main__":
    s = Shelf()
    # b = Book(74521113921233320802,
    #          "Army of the Egyptian",
    #          "Saladin",
    #          "dasda Academy",
    #          "adsasd",
    #          2022,
    #          29)
    # s.add_book(b)
    # s.edit_book(id=2, isbn=80021113921231300002,author="Cyrus",name="Army of Iranian")
    # s.remove_book(2)
    [print(i) for i in s.get_by_author("Darius")]
    print()
    # print(s)
