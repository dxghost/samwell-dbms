def validate_isbn(ISBN):
    if type(ISBN) != int:
        raise TypeError(
            "Invalid data for ISBN. can't assign type `%s` to int." % (type(ISBN)))
    if len(str(ISBN)) != 20:
        raise ValueError(
            "ISBN digits should be 20, given %s." % (len(str(ISBN))))
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
