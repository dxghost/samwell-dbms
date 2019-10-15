from core.settings import BOOK_ISBN_INDEX
import json
# TODO Generalize functions


def validate_isbn(ISBN):
    if type(ISBN) != int:
        raise TypeError(
            "Invalid data for ISBN. can't assign type `%s` to int." % (type(ISBN)))
    if len(str(ISBN)) != 20:
        raise ValueError(
            "ISBN digits should be 20, given %s." % (len(str(ISBN))))
    with open(BOOK_ISBN_INDEX, 'r') as book_isbn_table:
        current_isbns = json.load(book_isbn_table)
    if str(ISBN) in current_isbns:
        raise ValueError(
            "There already exists a book with given ISBN %d." % (ISBN))
    return True


def validate_name(name):
    if type(name) != str:
        raise TypeError(
            "Invalid data for book name. can't assign type `%s` to str." % (type(name)))
    if len(name) > 200:
        raise ValueError(
            "book name should be at most 200 characters, given %s." % (len(str(name))))
    return True


def validate_author(author):
    if type(author) != str:
        raise TypeError(
            "Invalid data for author. can't assign type `%s` to str." % (type(author)))
    if len(author) > 200:
        raise ValueError(
            "author should be at most 200 characters, given %s." % (len(str(author))))


def validate_publisher(publisher):
    if type(publisher) != str:
        raise TypeError(
            "Invalid data for publisher. can't assign type `%s` to str." % (type(publisher)))
    if len(publisher) > 200:
        raise ValueError(
            "publisher should be at most 200 characters, given %s." % (len(str(publisher))))
    return True


def validate_subject(subject):
    if type(subject) != str:
        raise TypeError(
            "Invalid data for subject. can't assign type `%s` to str." % (type(subject)))
    if len(subject) > 100:
        raise ValueError(
            "subject should be at most 100 characters, given %s." % (len(str(subject))))
    return True


def validate_publish_year(published_year):
    if type(published_year) != int:
        raise TypeError("Invalid data for published_year. can't assign type `%s` to int." % (
            type(published_year)))
    if len(str(published_year)) != 4:
        raise ValueError("published_year digits should be 4, given %s." % (
            len(str(published_year))))
    return True


def validate_pages_count(pages_count):
    if type(pages_count) != int:
        raise TypeError("Invalid data for pages_count. can't assign type `%s` to int." % (
            type(pages_count)))
    if len(str(pages_count)) > 4:
        raise ValueError(
            "pages_count digits should be at most 4, given %s." % (len(str(pages_count))))
    return True


def validate_publisher_number(pub_no):
    if type(pub_no) != int:
        raise TypeError("Invalid data for publisher number. can't assign type `%s` to int." % (
            type(pub_no)))
    if len(str(pub_no)) != 6:
        raise ValueError(
            "Publisher number digits should be 6, given %s." % (len(str(pub_no))))
    return True


def validate_publisher_name(pub_name):
    if type(pub_name) != str:
        raise TypeError(
            "Invalid data for publisher name. can't assign type `%s` to str." % (type(pub_name)))
    if len(pub_name) > 200:
        raise ValueError(
            "Publisher name should be at most 200 characters, given %s." % (len(str(pub_name))))
    return True


def validate_publisher_field(pub_field):
    if type(pub_field) != str:
        raise TypeError(
            "Invalid data for publisher field. can't assign type `%s` to str." % (type(pub_field)))
    if len(pub_field) > 200:
        raise ValueError(
            "Publisher field should be at most 200 characters, given %s." % (len(str(pub_field))))
    return True


def validate_publisher_manager_name(pub_manager):
    if type(pub_manager) != str:
        raise TypeError(
            "Invalid data for publisher manager name. can't assign type `%s` to str." % (type(pub_manager)))
    if len(pub_manager) > 100:
        raise ValueError(
            "publisher manager name should be at most 100 characters, given %s." % (len(str(pub_manager))))
    return True


def validate_publisher_address(pub_addr):
    if type(pub_addr) != str:
        raise TypeError(
            "Invalid data for publisher address. can't assign type `%s` to str." % (type(pub_addr)))
    if len(pub_addr) > 200:
        raise ValueError(
            "Publisher address should be at most 200 characters, given %s." % (len(str(pub_addr))))
    return True


def validate_publisher_books(pub_books):
    if type(pub_books) != list:
        raise TypeError(
            "Invalid data for published books. cant assign type %s to list." % (
                type(pub_books)))
    for i in pub_books:
        if type(i) != int:
            raise TypeError(
                "Invalid data for published book id. cant assign type %s to int." % (
                    type(i))
            )
    return True
