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

    def serialize(self):
        if self.is_leaf():
            return {
                "phrase_id": self.phrase_id,
                "val": self.val,
                "function": self.function,
                "feature_or_phrase_type": self.feature_or_phrase_type,
                "word_root": self.word_root
            }
        return {
            "phrase_id": self.phrase_id,
            "val": self.val,
            "function": self.function,
            "feature_or_phrase_type": self.feature_or_phrase_type,
            "word_root": self.word_root,
            "children": [child.serialize() for child in self.children]
        }

    @staticmethod
    def deserialize(data):
        if not data:
            return None
        node = ConstituencyTreeNode(data["phrase_id"], data["val"], data["function"], data["feature_or_phrase_type"], data["word_root"])
        if "children" in data:
            node.children = [ConstituencyTreeNode.deserialize(child) for child in data["children"]]
        else:
            node.children = []
        return node

    def to_vector(self):
        if self.is_leaf():
            return f'()'
        return f'({"".join([child.to_vector() for child in self.children])})'


def build(word_list : []) -> ConstituencyTreeNode:
    if not word_list:
        return ConstituencyTreeNode("", "", "", "", "")

    sentence = " ".join([word["word"] for word in word_list])
    root = ConstituencyTreeNode("", sentence, "","s", "")

    dict = {}
    for word in word_list:
        id = word["phrase_id"]
        dict.setdefault(id, []).append(word)

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

    def __init__(self, pasuk_id):
        self.root = None
        self.pasuk_id = pasuk_id
        self.psukiot = None
        self.roots = None
        self.characteristic = None

    def build_tree(self):
        words, psukiot, roots, characteristic = get_pasuk_parsed(self.pasuk_id)
        self.root = build(words)
        self.psukiot = psukiot
        self.roots = roots
        self.characteristic = characteristic


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

    def serialize(self):
        return {
            "pasuk_id": self.pasuk_id,
            "root": self.root.serialize() if self.root else None
        }

    @staticmethod
    def deserialize(data):
        pasuk_id = data["pasuk_id"]
        tree = ConstituencyTree(pasuk_id)
        tree.root = ConstituencyTreeNode.deserialize(data["root"])
        return tree

    def to_vector(self):
        return self.root.to_vector() if self.root else None

    def average_children(self, node):
        if not node.children:
            return 0
        num_children = len(node.children)
        child_factors = [self.__average_branching_factor(child) for child in node.children]
        return (num_children + sum(child_factors)) / (1 if not node.is_leaf() else len(node.children))

    def average_children(self):
        total_children, total_nodes = self.__average_children(self.root)
        return total_children / total_nodes if total_nodes > 0 else 0

    def __average_children(self, node):
        if not node.children:
            return 0, 0  # No children and not an internal node

        num_children = len(node.children)
        total_children = num_children
        total_nodes = 1  # Current node is counted as a node with children

        for child in node.children:
            child_children, child_nodes = self.__average_children(child)
            total_children += child_children
            total_nodes += child_nodes

        return total_children, total_nodes

    def max_children(self):
        return self.__max_children(self.root)

    def __max_children(self, node):
        if not node:
            return 0

        num_children = len(node.children)
        max_children_descendants = max((self.__max_children(child) for child in node.children), default=0)
        return max(num_children, max_children_descendants)