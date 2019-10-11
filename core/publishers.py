# TODO implement publisher class
# TODO apply constraints to init
# TODO implement queries/stores
from validators import validate_publisher_number, validate_publisher_name, validate_publisher_field, validate_publisher_manager_name, validate_publisher_address, validate_publisher_books
from settings import PUBLISHERS_DATABASE_PATH

class Publisher:
    def __init__(self, pub_no, pub_name, pub_field, pub_manager, pub_addr,pub_books, admin=False):
        if admin == False:
            validate_publisher_number(pub_no)
            validate_publisher_name(pub_name)
            validate_publisher_field(pub_field)
            validate_publisher_manager_name(pub_manager)
            validate_publisher_address(pub_addr)
            validate_publisher_books(pub_books)
        self.number = pub_no
        self.name = pub_name
        self.field = pub_field
        self.manager_name = pub_manager
        self.address = pub_addr
        self.published_books = pub_books

    def as_dictionary(self):
        return({
            "Number": self.number,
            "Name": self.name,
            "Field": self.field,
            "Manager": self.manager_name,
            "Address": self.address
        })

    def __str__(self):
        # TODO show publishers books
        print("")
        print("Publisher Number:        %s" % (self.number))
        print("Publisher Name:          %s" % (self.name))
        print("Publisher Field:         %s" % (self.field))
        print("Publisher Manager:       %s" % (self.manager_name))
        print("Publisher Address:            %s" % (self.address))
        return ""

class PublishingMinistry:
    def __init__(self):
        self.publishers = {}
        self.publishers_books_data = {}
