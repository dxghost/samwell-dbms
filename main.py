# TODO intialize and load json files into ram
# TODO start terminal listener
from core.books import Shelf, Book
from core.publishers import PublishingMinistry, Publisher


publishing_agent = PublishingMinistry()
book_shelf = Shelf()
publishing_agent.set_book_shelf(book_shelf)
book_shelf.set_publishers_ministry(publishing_agent)

while True:
    publishing_agent.set_book_shelf(book_shelf)
    book_shelf.set_publishers_ministry(publishing_agent)

    instruction = input("$ ")
    instruction = instruction.split()
    if len(instruction)==0:
        continue
    command = instruction[0]

    if command == "add_book":
        isbn = int(instruction[1])
        name = instruction[2]
        author = instruction[3]
        publisher = instruction[4]
        subject = instruction[5]
        published_year = int(instruction[6])
        pages_count = int(instruction[7])
        bk = Book(isbn, name, author, publisher,
                  subject, published_year, pages_count)
        book_shelf.add_book(bk)

    elif command == "edit_book":
        # TODO dynamic args
        id = int(instruction[1])
        isbn = int(instruction[2])
        name = instruction[3]
        author = instruction[4]
        publisher = instruction[5]
        subject = instruction[6]
        published_year = instruction[7]
        pages_count = instruction[8]
        book_shelf.edit_book(id, isbn, name, author, publisher,
                             subject, published_year, pages_count)

    elif command == "remove_book":
        id = int(instruction[1])
        book_shelf.remove_book(id)

    elif command == "get_book_by_exact_name":
        name = instruction[1]
        books = book_shelf.get_by_exact_name(name)
        [print(book) for book in books]

    elif command == "get_book_by_name":
        name = instruction[1]
        books = book_shelf.get_by_name(name)
        [print(book) for book in books]

    elif command == "get_book_by_subject":
        subject = instruction[1]
        books = book_shelf.get_by_subject(subject)
        [print(book) for book in books]

    elif command == "get_book_by_isbn":
        isbn = instruction[1]
        books = book_shelf.get_by_isbn(isbn)
        [print(book) for book in books]

    elif command == "get_book_by_author":
        author = instruction[1]
        books = book_shelf.get_by_author(author)
        [print(book) for book in books]

    elif command == "show_book_by_id":
        id = int(instruction[1])
        book_shelf.show_by_id(id)

    elif command == "add_publisher":
        pub_no = int(instruction[1])
        pub_name = instruction[2]
        pub_field = instruction[3]
        pub_manager = instruction[4]
        pub_addr = instruction[5]
        pb = Publisher(pub_no, pub_name, pub_field, pub_manager, pub_addr)
        publishing_agent.add_publisher(pb)

    elif command == "edit_publisher":
        # TODO dynamic args
        name = instruction[1]
        pub_no = int(instruction[2])
        pub_field = instruction[3]
        pub_manager = instruction[4]
        pub_addr = instruction[5]
        publishing_agent.edit_publisher(
            name, pub_no, pub_field, pub_manager, pub_addr)
    elif command == "remove_publisher":
        name = instruction[1]
        publishing_agent.remove_publisher(name)

    elif command == "show_publisher_by_exact_name":
        name = instruction[1]
        publishing_agent.show_publisher(name)

    elif command == "show_publisher_by_name":
        name = instruction[1]
        publishers = publishing_agent.get_by_name(name)
        [print(publisher) for publisher in publishers]
    else:
        print("[Error] Undefined command %s." % (command))

# print(book_shelf)
# b = Book(
#     82521113921233320802,
#     "Army of the Love",
#     "Night Lover",
#     "GHLMCH",
#     "Fight",
#     2031,
#     10
# )
# book_shelf.add_book(b)

# p = Publisher(
#     812312,
#     "GHLMCH",
#     "Academics",
#     "kzm ghlmch",
#     "Enghelab",
# )
# publishing_agent.add_publisher(p)

# book_shelf.edit_book(id=3, publisher="GHLMCH")
# book_shelf.remove_book(4)
# book_shelf.show_by_id(5)
# publishing_agent.edit_publisher("GAJ",pub_no=999999,pub_field="JANGI",pub_addr="Nezam Abad",pub_manager="Reza Pishro")
# publishing_agent.remove_publisher("GHLMCH")
# publishing_agent.show_publisher("GHLMCH")
# add_book 82521113921233320802 "Army" "Armin" "GAJ" "Edu" 2001 2
# add_publisher 812312 GAJ Academics ghlmch Enghelab
