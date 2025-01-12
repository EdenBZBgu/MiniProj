from transformers import AutoModel, AutoTokenizer

from Classes.Pasuk import Pasuk
from Classes.Torah import Torah
from ExternalData.dependency_parser import get_pasuk_encoded_dependency, load_torah_dependency
from ExternalData.root_model import RootSVMClassifier, RootLogisticRegressionClassifier, RootRidgeClassifierModel, \
    RootKNNClassifier, RootMLPClassifierModel
from ExternalData.statistics import calculate_word_frequencies_by_book, calculate_word_frequencies_by_teuda, \
    calculate_phraseText_frequencies_byBook, calculate_pasuk_lengths_by_book, calculate_unique_word_counts_by_book, \
    calculate_tree_depths
import pandas as pd

from ExternalData.teamim_model import TeamimSVMClassifier, TeamimLogisticRegressionClassifier, \
    TeamimRidgeClassifierModel, TeamimKNNClassifier, TeamimMLPClassifierModel


def main():
    t = Torah()
    t.read("ExternalData/torah_update.xlsx")
    t.parse_trees()
    t.save()

    # t2 = Torah()
    # t2.load()

    # pasuk = [p for p in t2.books[0].psukim if p._pasuk_id == 'Tanakh.Torah.Genesis.22.1'][0]
    # pasuk.dependency_tree.print_tree()
    # pasuk.constituency_tree.print_tree()
    # pasuk.teamim_tree.print_tree()

    # TeamimClassifier1 = TeamimSVMClassifier(t2, isBook=False)
    # TeamimClassifier1.cross_validate()
    #
    # TeamimClassifier2 = TeamimLogisticRegressionClassifier(t2, isBook=False)
    # TeamimClassifier2.cross_validate()
    #
    # TeamimClassifier3 = TeamimRidgeClassifierModel(t2, isBook=False)
    # TeamimClassifier3.cross_validate()
    #
    # TeamimClassifier4 = TeamimKNNClassifier(t2, n_neighbors=1, isBook=False)
    # TeamimClassifier4.cross_validate()
    #
    # TeamimClassifier5 = TeamimMLPClassifierModel(t2, isBook=False)
    # TeamimClassifier5.cross_validate()

    # RootClassifier.train()
    # RootClassifier.test()
    #
    # Classifier = LogisticRegressionClassifier(t2)
    # Classifier.train()
    # Classifier.test()
    #
    # Classifier = RidgeClassifierModel(t2)
    # Classifier.train()
    # Classifier.test()

    # Classifier = KNNClassifier(t2, n_neighbors=2)
    # Classifier.train()
    # Classifier.test()
    #
    # Classifier = KNNClassifier(t2, n_neighbors=2, isBook=False)
    # Classifier.train()
    # Classifier.test()

    # Classifier = MLPClassifierModel(t2)
    # Classifier.train()
    # Classifier.test()
    #
    # Classifier = MLPClassifierModel(t2, isBook=False)
    # Classifier.train()
    # Classifier.test()


if __name__ == "__main__":
    main()
