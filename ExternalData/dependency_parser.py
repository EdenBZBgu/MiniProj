import re
import xml.etree.ElementTree as ET
from datetime import timedelta
from cachetools import TTLCache, cached
import torch

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
books = ["Genesis.xml", "Exodus.xml", "Leviticus.xml", "Numbers.xml", "Deuteronomy.xml"]


@cached(cache=TTLCache(maxsize=1, ttl=timedelta(hours=1).total_seconds()))
def process_book(file_path):
    book_dict = {}
    xml_tree = ET.parse("ExternalData/" + file_path)
    root = xml_tree.getroot()
    sentences = root.findall('.//tei:s', namespaces=namespaces)

    for sentence in sentences:
        sentence_id = sentence.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
        book_dict[sentence_id] = sentence

    return book_dict


@cached(cache=TTLCache(maxsize=1, ttl=timedelta(hours=1).total_seconds()))
def load_torah_dependency():
    torah_books_dict = {book: process_book(book) for book in books}
    return torah_books_dict


def get_pasuk_encoded_dependency(pasuk_id: str, dependency):
    for book_dict in dependency.values():
        if pasuk_id in book_dict:
            pasuk = book_dict[pasuk_id]
            w_tags = pasuk.findall(".//tei:w", namespaces=namespaces)
            sentence = ""
            for w_tag in w_tags:
                word = w_tag.attrib["dtoken"].split('_')[0]
                sentence = sentence + word + " "

            return sentence.strip()


def parse_pasuk_dicta_dependency(pasuk, model, tokenizer):
    result = model.predict([pasuk], tokenizer, output_style='json')

    if isinstance(result, list) and len(result) > 0:
        return result[0]

    raise ValueError("Unexpected format for the parsed output.")


def get_pasuk_parsed(pasuk_id: str, model, tokenizer):
    dependency = load_torah_dependency()
    pasuk = get_pasuk_encoded_dependency(pasuk_id, dependency)
    return parse_pasuk_dicta_dependency(pasuk, model, tokenizer)

