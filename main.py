# TODO intialize and load json files into ram
# TODO start terminal listener
from core.books import Shelf, Book
from core.publishers import PublishingMinistry, Publisher



publishing_agent = PublishingMinistry()
book_shelf = Shelf()
publishing_agent.set_book_shelf(book_shelf)
book_shelf.set_publishers_ministry(publishing_agent)


# print(book_shelf)
# b = Book(
#     82521113921233320802,
#     "Army of the Love",
#     "Night Lover",
#     "GAJ",
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