from collections import Counter

def calculate_word_frequencies(self):
    word_counter = Counter()
    for book in self.books:
        for pasuk in book.psukim:
            word_counter.update(pasuk.words())
    return word_counter

def calculate_phrase_frequencies(self, n=2):  # n: size of phrase (e.g., bigram = 2)
    phrase_counter = Counter()
    for book in self.books:
        for pasuk in book.psukim:
            words = pasuk.words()
            phrases = [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]
            phrase_counter.update(phrases)
    return phrase_counter



def calculate_pasuk_lengths(self):
    lengths = [len(pasuk.words()) for book in self.books for pasuk in book.psukim]
    return {
        "min": np.min(lengths),
        "max": np.max(lengths),
        "mean": np.mean(lengths),
        "median": np.median(lengths),
        "std_dev": np.std(lengths),
    }

def unique_words_per_pasuk(self):
    unique_word_counts = [
        len(set(pasuk.words())) for book in self.books for pasuk in book.psukim
    ]
    return unique_word_counts

def calculate_tree_depths(self):
    depths = {"dependency_tree": [], "teamim_tree": []}
    for book in self.books:
        for pasuk in book.psukim:
            if pasuk.dependency_tree:
                depths["dependency_tree"].append(pasuk.dependency_tree.depth())
            if pasuk.teamim_tree:
                depths["teamim_tree"].append(pasuk.teamim_tree.depth())
    return depths

def calculate_phrases_per_pasuk(self):
    phrase_counts = {"dependency_tree": [], "teamim_tree": []}
    for book in self.books:
        for pasuk in book.psukim:
            if pasuk.dependency_tree:
                phrase_counts["dependency_tree"].append(pasuk.dependency_tree.num_phrases())
            if pasuk.teamim_tree:
                phrase_counts["teamim_tree"].append(pasuk.teamim_tree.num_phrases())
    return phrase_counts

def encode_tree_patterns(self):
    patterns = {"dependency_tree": [], "teamim_tree": []}
    for book in self.books:
        for pasuk in book.psukim:
            if pasuk.dependency_tree:
                patterns["dependency_tree"].append(pasuk.dependency_tree.encode_structure())
            if pasuk.teamim_tree:
                patterns["teamim_tree"].append(pasuk.teamim_tree.encode_structure())
    return patterns
