# TODO implement a function which gives current ID and increments it
from core.settings import BOOKS_ID_TABLE
import json


def get_book_id():
    with open(BOOKS_ID_TABLE, "r") as book_id_file:
        book_id_data = json.load(book_id_file)
        book_id_data["CurrentID"] += 1
        usable_id = book_id_data["CurrentID"]
    with open(BOOKS_ID_TABLE, "w") as book_id_file:
        json.dump(book_id_data, book_id_file)
    return usable_id

if __name__ == "__main__":
    print(get_book_id())