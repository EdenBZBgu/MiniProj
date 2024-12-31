import os
import pickle
import pandas as pd
from typing import List

from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

from Classes.Pasuk import Pasuk

AUTOMODEL = AutoModel.from_pretrained('dicta-il/dictabert-tiny-joint', trust_remote_code=True)
AUTOMODEL.eval()
TOKENIZER = AutoTokenizer.from_pretrained('dicta-il/dictabert-tiny-joint')


class Book:
    def __init__(self, book_name, book_number):
        self.book_name: str = book_name
        self.book_number: int = book_number
        self.psukim: List[Pasuk] = []

    def serialize(self) -> dict:
        return {
            "book_name": self.book_name,
            "book_number": self.book_number,
            "psukim": [pasuk.serialize() for pasuk in self.psukim]
        }

    def deserialize(data):
        if not data:
           return None
        book = Book(data["book_name"], data["book_number"])
        book.psukim = [Pasuk.deserialize(pasuk) for pasuk in data["psukim"]]
        return book


class Teuda:
    def __init__(self, teuda_name):
        self.teuda_name: str = teuda_name
        self.psukim: List[Pasuk] = []

class Torah:
    def __init__(self):
        self.books: List[Book] = []
        self.teudot: List[Teuda] = []

    def read(self, filename: str):
        print(f"Reading {filename}\n")
        tanach_raw = pd.read_excel(filename)
        # tanach_raw = tanach_raw[tanach_raw['Book'] == 'Genesis']
        # tanach_raw = tanach_raw[tanach_raw['Text'] == 'בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃']
        for _, row in tanach_raw.iterrows():
            book_name = row["Book"]
            book_number = row["BookNumber"]
            teuda_name = row["Teuda"]
            chapter = row["Chapter"]
            pasuk_number = row["Pasuk"]
            pasuk_text = row["Text"]
            pasuk_id = row["Pasuk ID"]

            if book_number > len(self.books):
                self.books.append(Book(book_name, book_number))

            pasuk = Pasuk(pasuk_id, pasuk_text, book_name)
            self.books[book_number - 1].psukim.append(pasuk)

            teuda_obj = next((teuda for teuda in self.teudot if teuda.teuda_name == teuda_name), None)
            if not teuda_obj:
                teuda_obj = Teuda(teuda_name)
                self.teudot.append(teuda_obj)
            teuda_obj.psukim.append(pasuk)

    def parse_trees(self):
        for book in self.books:
            print(f"Parsing book {book.book_name}")
            for pasuk in tqdm(book.psukim):
                pasuk.build_teamim_tree()
                pasuk.build_constituency_tree()
                pasuk.build_dependency_tree(AUTOMODEL, TOKENIZER)

    def save(self, filename: str = "torah.pkl"):
        with open(filename, "wb") as f:
            pickle.dump({"books": self.books, "teudot": self.teudot}, f)

    def load(self, filename: str = "torah.pkl"):
        with open(filename, "rb") as f:
            data = pickle.load(f)
            self.books = data["books"]
            self.teudot = data["teudot"]
