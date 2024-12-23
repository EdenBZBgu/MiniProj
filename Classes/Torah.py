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
    def __init__(self, book_name, book_number, teuda_number):
        self.book_name: str = book_name
        self.book_number: int = book_number
        self.tedua_number: int = teuda_number
        self.psukim: List[Pasuk] = []

    def serialize(self) -> dict:
        return {
            "book_name": self.book_name,
            "book_number": self.book_number,
            "tedua_number": self.tedua_number,
            "psukim": [pasuk.serialize() for pasuk in self.psukim]
        }

    def deserialize(self, data):
        if not data:
           return None
        book = Book(data["book_name"], data["book_number"], data["tedua_number"])
        book.psukim = [Pasuk.deserialize(pasuk) for pasuk in data["psukim"]]
        return book


class Torah:
    def __init__(self):
        self.books: List[Book] = []

    def read(self, filename: str):
        tanach_raw = pd.read_excel(filename)
        for _, row in tanach_raw.iterrows():
            book_name, book_number, teuda_number, chapter, pasuk_number, pasuk_text = row
            if book_number > len(self.books):
                self.books.append(Book(book_name, book_number, teuda_number))

            pasuk = Pasuk(f"Tanakh.Torah.{book_name}.{chapter}.{pasuk_number}", pasuk_text)
            self.books[book_number - 1].psukim.append(pasuk)

    def parse_trees(self):
        for book in self.books:
            print(f"Parsing book {book.book_name}")
            for pasuk in tqdm(book.psukim):
                pasuk.build_teamim_tree()
                pasuk.build_constituency_tree()
                pasuk.build_dependency_tree(AUTOMODEL, TOKENIZER)

    def save(self, filename: str):
        with open(filename, "w") as f:
            pickle.dump([book.serialize() for book in self.books], f)

    def load(self, filename: str):
        with open(filename, "r") as f:
            self.books = pickle.load(f)

