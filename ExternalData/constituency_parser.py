import re


# @cached(cache=TTLCache(maxsize=1, ttl=600))
def main():
    # xml = etree.parse("Genesis.xml")
    # xml = xml.getroot()[1][0]  # Text region, Genesis Book
    #
    # for chapter in xml:
    #     for s in chapter:
    #

    import xml.etree.ElementTree as ET

    class WordNode:
        def __init__(self, word_id, word, lemma, root, pos):
            self.word_id = word_id  # Unique identifier for the word
            self.word = word  # The word itself
            self.root = root  # Root of the word (if applicable)
            self.head = None  # The head word (e.g., the predicate or parent word in the tree)
            self.dep_type = None  # Dependency type (subject, object, etc.)

        def set_head(self, head, dep_type):
            """Set the head of the word and its dependency type."""
            self.head = head
            self.dep_type = dep_type

        def __str__(self):
            """Return a string representation of the word and its dependency."""
            return f"{self.word} ({self.dep_type}) -> {self.head.word if self.head else None}"

    class DependencyTree:
        def __init__(self):
            self.nodes = {}  # A dictionary to hold all the word nodes
            self.roots = []  # List of root nodes

        def add_node(self, word_id, word, lemma, root, pos):
            """Add a new word node to the tree."""
            node = WordNode(word_id, word, lemma, root, pos)
            self.nodes[word_id] = node
            return node

        def add_dependency(self, child_id, head_id, dep_type):
            """Establish a dependency relation between words."""
            child_node = self.nodes.get(child_id)
            head_node = self.nodes.get(head_id)

            if child_node and head_node:
                child_node.set_head(head_node, dep_type)

        def set_roots(self, root_ids):
            """Set the root words of the tree."""
            for root_id in root_ids:
                root_node = self.nodes.get(root_id)
                if root_node:
                    self.roots.append(root_node)

        def __str__(self):
            """Return a string representation of the entire dependency tree."""
            tree_str = []
            for node in self.nodes.values():
                tree_str.append(str(node))
            return "\n".join(tree_str)

    # Sample XML Data (replace this with your actual XML content
    xml_tree = ET.parse("Genesis.xml")

    # Parse the XML
    root = xml_tree.getroot()
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    sentences = root.findall('.//tei:s', namespaces=namespaces)

    for sentence in sentences:
        w_tags = sentence.findall(".//tei:w", namespaces=namespaces)
        phrases = sentence.findall(".//tei:phrase", namespaces=namespaces)

        for w_tag in w_tags:
            # print(w_tag.attrib["dtoken"])
            word = w_tag.attrib["dtoken"].split('_')[0]
            root = re.sub(r'[^\u0590-\u05FF]$', '', w_tag.attrib["lemma"])
            # print(word)
            # job = w_tag.attrib["dtoken"].split('_')[-2]
            job = w_tag.attrib["dtoken"].rsplit('_', 1)[]
            print(job)
            phrase_id = w_tag.findall(".//tei:m", namespaces=namespaces)
            for id in phrase_id:
                if "phraseId" in id.attrib:
                    pass
                    # print(id.attrib["phraseId"])
        input("stop")


if __name__ == "__main__":
    main()
