from ExternalData.teamim_parser import get_pasuk_encoded_teamim
from Classes.BaseTree import BaseTree
from typing import List

Emperors = {
    #     "00": "Siluk",
    "92": "Atnachta"
}
Kings = {
    "01": "Segol",
    "65": "Shalshelet",
    "80": "Zaqef qatan",
    "85": "Zaqef gadol",
    "73": "Tipcha",
}
Dukes = {"81": "Revii", "03": "Pashta", "02": "Zarka", "10": "Yetiv", "91": "Tevir"}
Counts = {
    "83": "Pazer",
    "84": "Karnei Para",
    "14": "Telisha Gedolah",
    "11": "Geresh",
    "62": "Gershayim",
    "98": "Munach L'Garmeih",
}

Hierarchy = [Emperors, Kings, Dukes, Counts]


class TeaminTreeNode:
    def __init__(self, symbols: List[str], text=""):
        self.symbols = symbols
        self.text = text
        self.left = None
        self.right = None

    def __str__(self):
        if self.left:
            return "[" + str(self.left) + str(self.right) + "]"
        return "[" + "/".join(self.symbols) + "]"

    def print_tree(self, prefix="", is_left=True, is_root=False):
        if is_root:
            connector = "   "
        else:
            connector = "├──" if is_left else "└──"

        if self.left or self.right:
            print(f"{prefix}{connector}")
            if self.left:
                self.left.print_tree(
                    prefix + ("|  " if is_left and not is_root else "   "), True
                )
            if self.right:
                self.right.print_tree(
                    prefix + ("|  " if is_left and not is_root else "   "), False
                )
        else:
            print(f"{prefix}{connector}[{'/'.join(self.symbols)}]")

    def height(self):
        if not self.left and not self.right:
            return 0
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        return 1 + max(left_height, right_height)

    def size(self):
        if not self.left and not self.right:
            return 1
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return 1 + left_size + right_size

    def serialize(self):
        if not self.left and not self.right:
            return {"symbols": self.symbols}
        return {
            "symbols": self.symbols,
            "left": self.left.serialize() if self.left else None,
            "right": self.right.serialize() if self.right else None,
        }

    @staticmethod
    def deserialize(data):
        if not data:
            return None
        node = TeaminTreeNode(data["symbols"])
        node.left = TeaminTreeNode.deserialize(data.get("left"))
        node.right = TeaminTreeNode.deserialize(data.get("right"))
        return node

    def to_vector(self):
        if not self.left and not self.right:
            return '()'
        return f'({self.left.to_vector()}{self.right.to_vector()})'


class TeamimTree(BaseTree):
    def __init__(self, pasuk_id, text=""):
        self.pasuk_id = pasuk_id
        self.root = None

    def build_tree(self):
        encoded_teamim = get_pasuk_encoded_teamim(self.pasuk_id)
        symbols = [w for w in encoded_teamim.split("/") if w]
        self.root = self.build(TeaminTreeNode(symbols))

    def build(self, node: TeaminTreeNode) -> TeaminTreeNode:
        for level in Hierarchy:
            for symbol in level:
                if (
                    symbol in node.symbols
                    and node.symbols.index(symbol) != len(node.symbols) - 1
                ):
                    node.left = self.build(
                        TeaminTreeNode(node.symbols[: node.symbols.index(symbol) + 1])
                    )
                    node.right = self.build(
                        TeaminTreeNode(node.symbols[node.symbols.index(symbol) + 1 :])
                    )
                    return node
        return node

    def height(self):
        if not self.root:
            return 0
        return self.root.height()

    def size(self):
        if not self.root:
            return 0
        return self.root.size()

    def print_tree(self):
        if not self.root:
            return "No tree"
        return self.root.print_tree(is_root=True)

    def serialize(self):
        return self.root.serialize()

    @staticmethod
    def deserialize(data):
        root = TeaminTreeNode.deserialize(data)
        return root

    def to_vector(self):
        return self.root.to_vector()
