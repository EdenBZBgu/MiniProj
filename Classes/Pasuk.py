from Classes.ConstituencyTree import ConstituencyTree
from Classes.DependencyTree import DependencyTree
from Classes.TeamimTree import TeamimTree


class Pasuk:
    def __init__(self, pasuk_id="", text=""):
        self.text: str = text
        self._pasuk_id: str = pasuk_id
        self._words: list[str] = text.split(" ")
        self._word_count: int = len(self._words)
        self.teamim_tree: TeamimTree = None
        self.constituency_tree: ConstituencyTree = None
        self.dependency_tree: DependencyTree = None

    def build_teamim_tree(self):
        self.teamim_tree = TeamimTree(self._pasuk_id)

    def build_constituency_tree(self):
        pass

    def build_dependency_tree(self):
        pass

    def text(self):
        return self.text

    def _id(self):
        return self._pasuk_id

    def words(self):
        return self._words

    def word_count(self):
        return self._word_count
