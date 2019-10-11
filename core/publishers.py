# TODO implement edit_publishers and remove_publishers
# TODO implement queries
from validators import validate_publisher_number, validate_publisher_name, validate_publisher_field, validate_publisher_manager_name, validate_publisher_address, validate_publisher_books
from settings import PUBLISHERS_DATABASE_PATH
import json


class Publisher:
    def __init__(self, pub_no, pub_name, pub_field, pub_manager, pub_addr, pub_books=[], admin=False):
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
            "Address": self.address,
            "Books": self.published_books
        })

    def __str__(self):
        print("")
        print("Publisher Number:                  %s" % (self.number))
        print("Publisher Name:                    %s" % (self.name))
        print("Publisher Field:                   %s" % (self.field))
        print("Publisher Manager:                 %s" % (self.manager_name))
        print("Publisher Address:                 %s" % (self.address))
        print("Publisher Published Books:         %s" % (self.published_books))
        return ""


class PublishingMinistry:
    def __init__(self):
        self.publishers = {}
        self.publishers_data = {}
        with open(PUBLISHERS_DATABASE_PATH, 'r') as publishers_table:
            self.publishers_data = json.load(publishers_table)
        for publisher_data in self.publishers_data.values():
            self.publishers[publisher_data["Name"]] = Publisher(
                pub_no=publisher_data["Number"],
                pub_name=publisher_data["Name"],
                pub_field=publisher_data["Field"],
                pub_manager=publisher_data["Manager"],
                pub_addr=publisher_data["Address"],
                pub_books=publisher_data["Books"],
                admin=True
            )

    def add_publisher(self, publisher):
        if(type(publisher) != Publisher):
            raise TypeError(
                "Only publisher instances are allowed, given %s." % (type(publisher)))
        name = publisher.name
        if name in self.publishers:
            raise ValueError(
                "There exists a publisher with given name %s" % (name))
        print("[add_publisher] Adding to Ministry.")
        print(publisher)
        self.publishers[name] = publisher
        self.publishers_data[name] = publisher.as_dictionary()

        self.sync_database(PUBLISHERS_DATABASE_PATH, self.publishers_data)
        print("------------------------------------------------------")

    def sync_database(self, file_path, data):
        print("[sync_database] Saving Changes to %s." % (file_path))
        with open(file_path, 'w') as database:
            json.dump(data, database)
        print("[sync_database] Changes saved to disk successfully.")
        print("-------------------------------------")

if __name__ == "__main__":
    m = PublishingMinistry()
    p = Publisher(
        212312,
        "GAJ",
        "Academics",
        "Ghasem Gaji",
        "Enghelab",
    )
    m.add_publisher(p)
