from transformers import AutoModel, AutoTokenizer

from Classes.Pasuk import Pasuk
from Classes.Torah import Torah
from ExternalData.dependency_parser import get_pasuk_encoded_dependency, load_torah_dependency
from ExternalData.statistics import calculate_word_frequencies_by_book, calculate_word_frequencies_by_teuda, \
    calculate_phraseText_frequencies_byBook, calculate_pasuk_lengths_by_book, calculate_unique_word_counts_by_book, \
    calculate_tree_depths
import pandas as pd
from ExternalData.model import Classifier, LogisticRegressionClassifier, SVMClassifier


def main():

    # t = Torah()
    # t.read("ExternalData/torah_update.xlsx")
    # t.parse_trees()
    # t.save()

    t2 = Torah()
    # t2.load()

    Classifier = SVMClassifier(t2)
    Classifier.train()
    Classifier.test()



if __name__ == "__main__":
    main()
