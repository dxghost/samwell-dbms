from core.validators import validate_publisher_number, validate_publisher_name, validate_publisher_field, validate_publisher_manager_name, validate_publisher_address, validate_publisher_books
from core.settings import PUBLISHERS_DATABASE_PATH
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

    def update(self, table):
        if table == "PUBLISHERS":
            self.sync_database(PUBLISHERS_DATABASE_PATH, self.publishers_data)
        else:
            print("[Publisher update] Enter Correct table name.")
            print("[Publisher update] Choices are: PUBLISHER.")

    def set_book_shelf(self, shelf):
        self.shelf = shelf
        # print("[set_book_shelf] Book shelf set.")

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

        self.update("PUBLISHERS")
        print("------------------------------------------------------")

    def edit_publisher(self, name, pub_no=None, pub_field=None, pub_manager=None, pub_addr=None):
        if name not in self.publishers:
            raise ValueError("No publisher found named %s." % (name))
        publisher = self.publishers[name]
        if pub_no:
            validate_publisher_number(pub_no)
            publisher.number = pub_no
        if pub_field:
            validate_publisher_field(pub_field)
            publisher.field = pub_field
        if pub_manager:
            validate_publisher_manager_name(pub_manager)
            publisher.manager_name = pub_manager
        if pub_addr:
            validate_publisher_address(pub_addr)
            publisher.address = pub_addr
        self.publishers_data[publisher.name] = publisher.as_dictionary()
        self.update("PUBLISHERS")

    def sync_database(self, file_path, data):
        print("[sync_database] Saving Changes to %s." % (file_path))
        with open(file_path, 'w') as database:
            json.dump(data, database)
        print("[sync_database] Changes saved to disk successfully.")
        print("-------------------------------------")

    def remove_publisher(self, name):
        if name not in self.publishers:
            raise ValueError("No publisher found named %s." % (name))
        print("[remove_publisher] The publisher you ordered to remove:")
        publisher = self.publishers[name]
        print(publisher)
        for book_id in publisher.published_books:
            self.shelf.remove_book(int(book_id))

        del self.publishers[name]
        del self.publishers_data[name]
        self.update("PUBLISHERS")
        print("------------------------------------------------------")

    def get_by_name(self,name):
        publishers =[]
        for publisher in self.publishers:
            if name in publisher.name:
                publishers.append(publisher)

        return publishers

    def show_publisher(self, name):
        if name not in self.publishers:
            raise ValueError("No publisher found named %s." % (name))
        print(self.publishers[name])

if __name__ == "__main__":
    m = PublishingMinistry()
    p = Publisher(
        212312,
        "GHLMCH",
        "Academics",
        "Ghasem Gaji",
        "Enghelab",
    )
    m.add_publisher(p)
