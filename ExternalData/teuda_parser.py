
import xml.etree.ElementTree as ET
import os
from cachetools import cached, TTLCache

books = ["Genesis.DH.xml", "Exodus.DH.xml", "Leviticus.DH.xml", "Numbers.DH.xml", "Deuteronomy.DH.xml"]


def get_all_sentences_from_book(book_path):
    book_dict = {}
    xml_tree = ET.parse("ExternalData/" + book_path)
    root = xml_tree.getroot()
    tanach = root.find('./tanach')
    book = tanach.find('./book')
    book_name = os.path.splitext(book_path)[0].split(".")[0]

    for chapter in book.findall('./c'):
        chapter_number = chapter.get('n')  # Get chapter number
        for verse in chapter.findall('./v'):
            verse_number = verse.get('n')  # Get verse number
            s_value = verse.get('s')  # Get 's' attribute value
            key = f"{book_name}.{chapter_number}.{verse_number}"
            if key not in book_dict:
                book_dict[key] = s_value

    return book_dict


@cached(cache=TTLCache(maxsize=1, ttl=200))
def load_teuda():
    torah_books_dict = {book: get_all_sentences_from_book(book) for book in books}
    return torah_books_dict


def get_pasuk_teuda(pasuk_id: str):
    pasuk_id = ".".join(pasuk_id.split(".")[-3:])
    book_name = pasuk_id.split(".")[0] + ".DH.xml"
    dict = load_teuda()
    if book_name in dict:
        return dict[book_name].get(pasuk_id)

    return None

