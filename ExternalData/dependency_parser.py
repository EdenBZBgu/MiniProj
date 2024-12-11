import re
import xml.etree.ElementTree as ET
from transformers import AutoModel, AutoTokenizer
import torch

namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
books = ["Genesis.xml", "Exodus.xml", "Leviticus.xml", "Numbers.xml", "Deuteronomy.xml"]

def process_book(file_path):
    book_dict = {}
    xml_tree = ET.parse(file_path)
    root = xml_tree.getroot()
    sentences = root.findall('.//tei:s', namespaces=namespaces)

    for sentence in sentences:
        sentence_id = sentence.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
        book_dict[sentence_id] = sentence

    return book_dict


def load_torah_dependency():
    torah_books_dict = {book: process_book(book) for book in books}
    return torah_books_dict


def get_pasuk_encoded_dependency(pasuk_id: str, constituency):
    for book_dict in constituency.values():
        if pasuk_id in book_dict:
            pasuk = book_dict[pasuk_id]
            w_tags = pasuk.findall(".//tei:w", namespaces=namespaces)
            sentence = ""
            for w_tag in w_tags:
                word = w_tag.attrib["dtoken"].split('_')[0]
                sentence = sentence + word + " "

            return sentence.strip()


def parse_pasuk_dicta_dependency(pasuk, tokenizer = AutoTokenizer.from_pretrained('dicta-il/dictabert-tiny-joint'), model = AutoModel.from_pretrained('dicta-il/dictabert-tiny-joint', trust_remote_code=True).eval()):
    return model.predict([pasuk], tokenizer, output_style='json')

def get_pasuk_parsed(pasuk_id: str):
    constituency = load_torah_dependency()
    pasuk = get_pasuk_encoded_dependency(pasuk_id, constituency)
    return parse_pasuk_dicta_dependency(pasuk)

def main():
    constituency = load_torah_dependency()
    pasuk = get_pasuk_encoded_dependency("Tanakh.Torah.Genesis.1.1", constituency)
    parsed = parse_pasuk_dicta_dependency(pasuk)
    print(parsed)


if __name__ == "__main__":
    main()
