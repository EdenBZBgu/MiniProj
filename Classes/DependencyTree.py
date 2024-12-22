from Classes.BaseTree import BaseTree
from ExternalData.dependency_parser import get_pasuk_parsed


class DependencyTreeNode:

    def __init__(self, index: int, val: str, children, dependency):
        self.index = index
        self.val = val
        self.children = children
        self.dependency = dependency

    def serialize(self):
        if not self.children:
            return {
                "index": self.index,
                "val": self.val,
                "dependency": self.dependency
            }
        return {
            "index": self.index,
            "val": self.val,
            "dependency": self.dependency,
            "children": [child.serialize() for child in self.children]
        }

    @staticmethod
    def deserialize(data):
        if not data:
            return None
        node = DependencyTreeNode(data["index"], data["val"], [], data["dependency"])
        node.children = [DependencyTreeNode.deserialize(child) for child in data["children"]]
        return node


def build(dictaParsedPasuk) -> DependencyTreeNode:
    nodes = {}

    for idx, token in enumerate(dictaParsedPasuk['tokens']):
        nodes[idx] = DependencyTreeNode(
            index=idx,
            val=token['token'],
            children=[],
            dependency=None
        )

    for idx, token in enumerate(dictaParsedPasuk['tokens']):
        parent = token['syntax']['dep_head_idx']
        dependency = token['syntax']['dep_func']
        if parent != -1:
            nodes[parent].children.append(nodes[idx])
            nodes[idx].dependency = dependency

    root_idx = dictaParsedPasuk['root_idx']
    root = nodes[root_idx]
    root.dependency = 'root'

    return root


class DependencyTree(BaseTree):

    def __init__(self, pasuk_id):
        self.root = None
        self.pasuk_id = pasuk_id

    def build_tree(self):
        self.root = build(get_pasuk_parsed(self.pasuk_id))

    def height(self):

        def _calculate_height(node):
            if not node.children:
                return 1
            return 1 + max(_calculate_height(child) for child in node.children)

        return _calculate_height(self.root) if self.root else 0

    def size(self):

        def _calculate_size(node):
            if not node.children:
                return 1
            return 1 + sum(_calculate_size(child) for child in node.children)

        return _calculate_size(self.root) if self.root else 0


    def print_tree(self):

        def _print_subtree(node, level=0):
            print("    " * level + f"{node.val} (index: {node.index}, dep: {node.dependency if node.dependency else 'None'})")
            for child in node.children:
                _print_subtree(child, level + 1)

        if self.root:
            _print_subtree(self.root)
        else:
            print("Tree is empty.")

    def serialize(self):
        if not self.root:
            return None
        return self.root.serialize()

    @staticmethod
    def deserialize(data):
        root = DependencyTreeNode.deserialize(data)
        return root



