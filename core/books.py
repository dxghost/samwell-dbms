import json
from settings import BOOKS_DATABASE_PATH, BOOK_AUTHOR_INDEX, BOOK_ISBN_INDEX, BOOK_NAME_INDEX
from validators import validate_isbn, validate_name, validate_author, validate_publisher, validate_subject, validate_publish_year, validate_pages_count
from id_gen import get_book_id


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
                                      id=book["ID"],
                                      admin=True)

        with open(BOOK_AUTHOR_INDEX, 'r') as author_index_table:
            self.books_author_data = json.load(author_index_table)
        with open(BOOK_ISBN_INDEX, 'r') as isbn_index_table:
            self.books_isbn_data = json.load(isbn_index_table)
        with open(BOOK_NAME_INDEX, 'r') as name_index_table:
            self.books_name_data = json.load(name_index_table)

    def remove_book(self, id):
        print("[remove_book] The book you ordered to remove:")
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

        print("[edit_book] The current status of book:(after edition)")
        print(book)
        print((self.books_data.keys()))
        self.books_data[str(id)] = self.books[id].as_dictionary()
        self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
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

        self.books_isbn_data[book.isbn] = book.id
        self.sync_database(BOOKS_DATABASE_PATH, self.books_data)
        self.sync_database(BOOK_AUTHOR_INDEX, self.books_author_data)
        self.sync_database(BOOK_ISBN_INDEX, self.books_isbn_data)
        self.sync_database(BOOK_NAME_INDEX, self.books_name_data)
        print("------------------------------------------------------")

    def get_by_exact_name(self, book_name):
        if book_name in self.books_name_data:
            result = self.books_name_data[book_name]
            books = []
            if len(result) == 0:
                return "[get_by_exact_name] No book found named %s.(edited to another name or removed.)" % (book_name)
            for i in result:
                books.append(self.books[i])
            return books
        else:
            return "[get_by_exact_name] No book found named %s." % (book_name)

    def get_by_name(self, book_name):
        # TODO Implement partial
        pass

    def get_by_subject(self, subject):
        # TODO Implement partial
        pass

    def get_by_isbn(self, isbn):
        # TODO Implement exact
        pass

    def get_by_author(self, isbn):
        # TODO Implement partial
        pass

    def __str__(self):
        print("The books available in shelf:")
        for book in self.books:
            print(self.books[book])
        return ""


if __name__ == "__main__":
    s = Shelf(BOOKS_DATABASE_PATH)
    # b = Book(83521113921233320802,
    #          "Army of the Mongols",
    #          "Ghenghis",
    #          "dasda Academy",
    #          "adsasd",
    #          2022,
    #          29)
    # s.add_book(b)
    # s.edit_book(id=2, isbn=80021113921231300002,author="Cyrus",name="Army of Iranian")
    # s.remove_book(2)
    print(s.get_by_exact_name("Army of the Chinese"))
    print()
    print(s)
