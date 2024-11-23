from abc import ABC, abstractmethod


class BaseTree(ABC):
    @abstractmethod
    def height(self):
        """Returns the height of the tree"""
        raise NotImplementedError

    @abstractmethod
    def size(self):
        """Returns the number of nodes in the tree"""
        raise NotImplementedError

    @abstractmethod
    def print_tree(self):
        """Prints the tree"""
        raise NotImplementedError
