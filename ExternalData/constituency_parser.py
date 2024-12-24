import re
import xml.etree.ElementTree as ET
from datetime import timedelta

from cachetools import cached, TTLCache

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0',
              'xml': '{http://www.w3.org/XML/1998/namespace}'}
features = []

books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]


def get_all_sentences_from_book(book_path):
    book_dict = {}
    xml_tree = ET.parse("ExternalData/" + book_path + ".xml")
    root = xml_tree.getroot()
    sentences = root.findall('.//tei:s', namespaces=namespaces)

    for sentence in sentences:
        sentence_id = sentence.attrib.get(f"{namespaces['xml']}id")
        book_dict[sentence_id] = sentence

    return book_dict


@cached(cache=TTLCache(maxsize=1, ttl=timedelta(hours=1).total_seconds()))
def load_torah_constituency():
    torah_books_dict = {book: get_all_sentences_from_book(book) for book in books}
    return torah_books_dict


def parse_pasuk_constituency(pasuk):
    words = []
    phrases = pasuk.findall(".//tei:phrase", namespaces=namespaces)
    phrase_type_map = {
        phrase.attrib.get("id"): (phrase.attrib.get("type"), phrase.attrib.get("function"))
        for phrase in phrases if all(key in phrase.attrib for key in ["id", "type", "function"])
    }

    w_tags = pasuk.findall(".//tei:w", namespaces=namespaces)
    for w_tag in w_tags:
        m_tags = w_tag.findall(".//tei:m", namespaces=namespaces)
        phrase_id = m_tags[0].attrib["phraseId"] if m_tags else None

        word_data = {
            "word": w_tag.attrib["dtoken"].split('_')[0],
            "phrase_id": phrase_id,
            "root": re.sub(r'[^\u0590-\u05FF]$', '', w_tag.attrib["lemma"]),
            "phrase_type": phrase_type_map.get(phrase_id)[0] if phrase_id else None,
            "feature": w_tag.attrib["dtoken"].split('_')[3],
            "phrase_function": phrase_type_map.get(phrase_id)[1] if phrase_id else None
        }

        words.append(word_data)

    return words

def get_pasuk_parsed(pasuk_id: str):
    constituency = load_torah_constituency()
    book_name = pasuk_id.split(".")[2] + ".xml"
    book_num = books.index(book_name)
    return parse_pasuk_constituency(constituency[books[book_num]][pasuk_id]) if pasuk_id in constituency[books[book_num]] else None
