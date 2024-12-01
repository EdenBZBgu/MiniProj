from Classes.BaseTree import BaseTree
from ExternalData.constituency_parser import get_pasuk_parsed

class ConstituencyTreeNode:
    def __init__(self, phrase_id : str, val : str, function : str, feature_or_phrase_type : str, word_root : str):
        self.phrase_id = phrase_id
        self.val = val
        self.function = function
        self.feature_or_phrase_type = feature_or_phrase_type
        self.word_root = word_root
        self.children = []

    def is_leaf(self):
        return not self.children

    def __str__(self):
        pass


def build(word_list : []) -> ConstituencyTreeNode:
    if not word_list:
        return ConstituencyTreeNode("", "", "", "", "")

    # word_data = {
    #     "word"
    #     "phrase_id"
    #     "root"
    #     "phrase_type"
    #     "feature"
    #     "function"
    # }

def inner_build(word_list : [], phrase_id: str):
    phrase = " ".join([word["word"] for word in word_list])
    node = ConstituencyTreeNode(phrase_id, phrase, word_list[0]["function"], word_list[0]["phrase_type"], "")

    for word in word_list:
        node.children.append(ConstituencyTreeNode(phrase_id, word, "",
                             word_list[0]["feature"],
                             word_list[0]["root"]))

class ConstituencyTree(BaseTree):
    def print_tree(self):
        pass

    def __init__(self, pasuk_id, book_id):
        self.root = build(get_pasuk_parsed(book_id, pasuk_id))

    def height(self):
       return self.__height(self.root)

    def __height(self, node):
        if not node.children:
            return 1
        children_heights = [self.__height(child) for child in node.children]
        return 1 + max(children_heights)


    def size(self):
        return self.__size(self.root)

    def __size(self, node):
        if not node.children:
            return 1
        children_sizes = [self.__size(child) for child in node.children]
        return 1 + sum(children_sizes)

