from Classes.BaseTree import BaseTree
from ExternalData.dependency_parser import get_pasuk_parsed


class DependencyTreeNode:

    def __init__(self, index: int, val: str, children, dependency):
        self.index = index
        self.val = val
        self.children = children
        self.dependency = dependency

    # def serialize(self, seen_nodes=None, path=None):
    #     if seen_nodes is None:
    #         seen_nodes = set()  # Initialize a set to track visited nodes
    #     if path is None:
    #         path = []  # Initialize the path to track the hierarchy
    #
    #     # Add current node to path for tracking
    #     current_path = path + [self.index]
    #
    #     # Detect circular reference
    #     if id(self) in seen_nodes:
    #         print(f"Circular reference detected in path: {' -> '.join(map(str, current_path))}")
    #         print({
    #             "index": self.index,
    #             "val": self.val,
    #             "dependency": self.dependency,
    #             "children": "Circular reference detected"
    #         })
    #         return
    #
    #     seen_nodes.add(id(self))  # Mark current node as visited
    #
    #     # Base case: no children
    #     if not self.children:
    #         return {
    #             "index": self.index,
    #             "val": self.val,
    #             "dependency": self.dependency
    #         }
    #
    #     # Recursive case: serialize children
    #     return {
    #         "index": self.index,
    #         "val": self.val,
    #         "dependency": self.dependency,
    #         "children": [child.serialize(seen_nodes, current_path) for child in self.children]
    #     }

    # def serialize(self):
    #     if not self.children:
    #         return {
    #             "index": self.index,
    #             "val": self.val,
    #             "dependency": self.dependency
    #         }
    #     return {
    #         "index": self.index,
    #         "val": self.val,
    #         "dependency": self.dependency,
    #         "children": [child.serialize() for child in self.children]
    #     }

    def serialize(self, visited=None):
        if visited is None:
            visited = set()  # Initialize the visited set on the first call

        # Check if the current node has been visited
        if self in visited:
            return None  # Return None or an appropriate placeholder if the node is already visited

        # Mark the current node as visited
        visited.add(self)

        # Serialize the current node
        serialized_data = {
            "index": self.index,
            "val": self.val,
            "dependency": self.dependency
        }

        # If the node has children, serialize them as well
        if self.children:
            serialized_data["children"] = [child.serialize(visited) for child in self.children]

        return serialized_data

    @staticmethod
    def deserialize(data):
        if not data:
            return None
        node = DependencyTreeNode(data["index"], data["val"], [], data["dependency"])
        if "children" in data:
            node.children = [DependencyTreeNode.deserialize(child) for child in data["children"]]
        else:
            node.children = []
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

    def __init__(self, pasuk_id, automodel, tokenizer):
        self.root = None
        self.pasuk_id = pasuk_id
        self.model = automodel
        self.tokenizer = tokenizer

    def build_tree(self):
        self.root = build(get_pasuk_parsed(self.pasuk_id, self.model, self.tokenizer))

    def height(self):

        def _calculate_height(node, visited=set()):
            if node in visited:
                return 0
            visited.add(node)
            if not node.children:
                return 1
            return 1 + max(_calculate_height(child, visited) for child in node.children)

        return _calculate_height(self.root) if self.root else 0


    def size(self):

        def _calculate_size(node, visited=set()):
            if node in visited:
                return 0
            visited.add(node)
            if not node.children:
                return 1
            return 1 + sum(_calculate_size(child, visited) for child in node.children)

        return _calculate_size(self.root) if self.root else 0


    # def print_tree(self):
    #
    #     def _print_subtree(node, level=0):
    #         print("    " * level + f"{node.val} (index: {node.index}, dep: {node.dependency if node.dependency else 'None'})")
    #         for child in node.children:
    #             _print_subtree(child, level + 1)
    #
    #     if self.root:
    #         _print_subtree(self.root)
    #     else:
    #         print("Tree is empty.")

    def print_tree(self):
        def _print_subtree(node, level=0, visited=None):
            if visited is None:
                visited = set()  # Initialize the set on the first call
            if node in visited:
                print("    " * level + f"{node.val} (index: {node.index}, dep: {node.dependency}")
                return  # Skip already visited nodes to avoid cycles

            visited.add(node)  # Mark the current node as visited
            print("    " * level + f"{node.val} (index: {node.index}, dep: {node.dependency if node.dependency else 'None'})")

            for child in node.children:
                _print_subtree(child, level + 1, visited)

        if self.root:
            _print_subtree(self.root)
        else:
            print("Tree is empty.")

    def serialize(self):
        return {
            "pasuk_id": self.pasuk_id,
            "root": self.root.serialize() if self.root else None
        }

    @staticmethod
    def deserialize(data):
        pasuk_id = data["pasuk_id"]
        tree = DependencyTree(pasuk_id)
        tree.root = DependencyTreeNode.deserialize(data["root"])
        return tree

    def to_vector(self):
        pass



