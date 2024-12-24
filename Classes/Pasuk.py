from Classes.ConstituencyTree import ConstituencyTree
from Classes.DependencyTree import DependencyTree
from Classes.TeamimTree import TeamimTree
from ExternalData.teuda_parser import get_pasuk_teuda


class Pasuk:
    def __init__(self, pasuk_id="", text="", book=""):
        self.text: str = text
        self._pasuk_id: str = pasuk_id
        self._words: list[str] = text.split(" ")
        self._word_count: int = len(self._words)
        self.teamim_tree: TeamimTree = None
        self.constituency_tree: ConstituencyTree = None
        self.dependency_tree: DependencyTree = None
        self.book = book
        self.teuda = get_pasuk_teuda(pasuk_id)

    def build_teamim_tree(self):
        self.teamim_tree = TeamimTree(self._pasuk_id)
        self.teamim_tree.build_tree()

    def build_constituency_tree(self):
        self.constituency_tree = ConstituencyTree(self._pasuk_id)
        self.constituency_tree.build_tree()

    def build_dependency_tree(self, automodel, tokenizer):
        self.dependency_tree = DependencyTree(self._pasuk_id, automodel, tokenizer)
        self.dependency_tree.build_tree()

    def text(self):
        return self.text

    def _id(self):
        return self._pasuk_id

    def words(self):
        return self._words

    def word_count(self):
        return self._word_count

    def print_pasuk(self):
        print("text: " + self.text)
        print("id: " + self._pasuk_id)
        print("teuda: " + self.teuda)


    def serialize(self):
        return {
            "text": self.text,
            "pasuk_id": self._pasuk_id,
            "words": self._words,
            "word_count": self._word_count,
            "teamim_tree": self.teamim_tree.serialize() if self.teamim_tree else None,
            "constituency_tree": self.constituency_tree.serialize() if self.constituency_tree else None,
            "dependency_tree": self.dependency_tree.serialize() if self.dependency_tree else None,
            "book": self.book,
            "teuda": self.teuda if self.teuda else None
        }

    @staticmethod
    def deserialize(data):
        if not data:
            return None
        pasuk = Pasuk()
        pasuk._pasuk_id = data["pasuk_id"]
        pasuk.text = data["text"]
        pasuk._words = data["words"]
        pasuk._word_count = data["word_count"]
        pasuk.teamim_tree = TeamimTree.deserialize(data["teamim_tree"])
        pasuk.constituency_tree = ConstituencyTree.deserialize(data["constituency_tree"])
        pasuk.dependency_tree = DependencyTree.deserialize(data["dependency_tree"])
        pasuk.book = data["book"]
        pasuk.teuda = data["teuda"]
        return pasuk
