from BaseTree import BaseTree
from dependency_parser import get_pasuk_parsed


class DependencyTreeNode:

    def __init__(self, index: int, val: str, children, parent, dependency):
        self.index = index
        self.val = val
        self.children = children
        self.parent = parent
        self.dependency = dependency

def build(dictaParsedPasuk) -> DependencyTreeNode:

    nodes = {}

    for idx, token in enumerate(dictaParsedPasuk['tokens']):
        nodes[idx] = DependencyTreeNode(
            index=idx,
            val=token['token'],
            children=[],
            parent=None,
            dependency=None
        )

    for idx, token in enumerate(dictaParsedPasuk['tokens']):
        parent = token['syntax']['dep_head_idx']
        dependency = token['syntax']['dep_func']
        if parent != -1:
            nodes[idx].parent = parent
            nodes[parent].children.append(nodes[idx])
            nodes[idx].dependency = dependency

    root_idx = dictaParsedPasuk['root_idx']
    root = nodes[root_idx]
    root.dependency = 'root'

    return root


class DependencyTree(BaseTree):

    def __init__(self, pasuk_id):
        self.root = build(get_pasuk_parsed(pasuk_id))

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



