# TODO implement edit&delete methods
# TODO implement different queries
import json
from settings import BOOKS_DATABASE_PATH

class Book:
    def __init__(self, ISBN, name, author, publisher, subject, published_year, pages_count):
        # TODO support multi value for authors and subjects
        # ISBN
        if type(ISBN) != int:
            raise TypeError(
                "Invalid data for ISBN. can't assign type `%s` to int." % (type(ISBN)))
        if len(str(ISBN)) != 20:
            raise ValueError(
                "ISBN digits should be 20, given %s." % (len(str(ISBN))))
        self.isbn = ISBN

        # NAME
        if type(name) != str:
            raise TypeError(
                "Invalid data for book name. can't assign type `%s` to str." % (type(name)))
        if len(subject) > 200:
            raise ValueError(
                "book name should be at most 200 characters, given %s." % (len(str(name))))
        self.name = name

        # AUTHOR
        if type(author) != str:
            raise TypeError(
                "Invalid data for author. can't assign type `%s` to str." % (type(author)))
        if len(author) > 200:
            raise ValueError(
                "author should be at most 200 characters, given %s." % (len(str(author))))
        self.author = author

        # PUBLISHER
        if type(publisher) != str:
            raise TypeError(
                "Invalid data for publisher. can't assign type `%s` to str." % (type(publisher)))
        if len(publisher) > 200:
            raise ValueError(
                "publisher should be at most 200 characters, given %s." % (len(str(publisher))))
        self.publisher = publisher

        # SUBJECT
        if type(subject) != str:
            raise TypeError(
                "Invalid data for subject. can't assign type `%s` to str." % (type(subject)))
        if len(subject) > 100:
            raise ValueError(
                "subject should be at most 100 characters, given %s." % (len(str(subject))))
        self.subject = subject

        # PUBLISHED YEAR
        if type(published_year) != int:
            raise TypeError("Invalid data for published_year. can't assign type `%s` to int." % (
                type(published_year)))
        if len(str(published_year)) != 4:
            raise ValueError("published_year digits should be 4, given %s." % (
                len(str(published_year))))
        self.published_year = published_year

        # PAGES COUNT
        if type(pages_count) != int:
            raise TypeError("Invalid data for pages_count. can't assign type `%s` to int." % (
                type(pages_count)))
        if len(str(pages_count)) > 4:
            raise ValueError(
                "pages_count digits should be at most 4, given %s." % (len(str(pages_count))))
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
                # TODO Add to BookISBN indexing

    def remove_book(self, id):
        print("The book you ordered to remove:")
        print(self.books[id-1])
        del self.books[id-1]
        del self.books_data[id-1]

    def add_book(self, book):
        if(type(book) != Book):
            raise TypeError(
                "Only book instances are allowed, given %s." % (type(book)))
        print(book)
        print("Adding to Shelf.")
        self.books.append(book)
        self.books_data.append(book.as_dictionary())
        print("Saving added book to file.")
        with open(BOOKS_DATABASE_PATH, 'w') as books_database:
            json.dump(self.books_data, books_database)

    def __str__(self):
        print("The books available in shelf:")
        for book in self.books:
            print(book)
        return ""


if __name__ == "__main__":
    s = Shelf(BOOKS_DATABASE_PATH)
    b = Book(96521119921231300000,
             "Mahdi's Story",
             "Mahdi DXi",
             "Ghost Academy",
             "Bio",
             1999,
             21)
    # s.add_book(b)
    print()
    print(s)
