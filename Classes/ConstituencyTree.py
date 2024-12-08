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

    sentence = " ".join([word["word"] for word in word_list])
    root = ConstituencyTreeNode("", sentence, "","s", "")

    dict = {}
    for word in word_list:
        id = word["phrase_id"]
        dict.setdefault(id, []).append(word)
        # if id in dict:
        #     dict[id] = dict[id].append(word)
        # else:
        #     dict[id] = [word]

    for id in dict:
        root.children.append(inner_build(dict[id],id))

    return root

def inner_build(word_list : [], phrase_id: str):
    phrase = " ".join([word["word"] for word in word_list])
    node = ConstituencyTreeNode(phrase_id, phrase, word_list[0]["phrase_function"], word_list[0]["phrase_type"], "")

    for i, word in enumerate(word_list):
        node.children.append(ConstituencyTreeNode(phrase_id, word, "",
                             word_list[i]["feature"],
                             word_list[i]["root"]))
    return node

class ConstituencyTree(BaseTree):
    def print_tree(self):
        if not self.root:
            print("(empty tree)")
            return
        self.__print_tree(self.root, 0)

    def __print_tree(self, node, level):
        # Indent based on the level of the node
        indent = "  " * level
        print(f"{indent}{node.phrase_id} ({node.feature_or_phrase_type}): {node.val}")

        for child in node.children:
            self.__print_tree(child, level + 1)

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

