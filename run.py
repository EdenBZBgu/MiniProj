from Classes.Torah import Torah
from ExternalData.Models.characteristic_model import CharacteristicSVMClassifier, CharacteristicRidgeClassifierModel, \
    CharacteristicKNNClassifier, CharacteristicLogisticRegressionClassifier, CharacteristicMLPClassifierModel, \
    CharacteristicSGDClassifierModel
from ExternalData.Models.characteristic_words_model import WCharacteristicSVMClassifier, \
    WCharacteristicRidgeClassifierModel, \
    WCharacteristicKNNClassifier, WCharacteristicMLPClassifierModel, WCharacteristicLogisticRegressionClassifier, \
    WCharacteristicSGDClassifierModel
from ExternalData.Models.consistuency_tree_model import ConstituencyTreeSVMClassifier, \
    ConstituencyTreeLogisticRegressionClassifier, ConstituencyTreeRidgeClassifierModel, ConstituencyTreeKNNClassifier, \
    ConstituencyTreeMLPClassifierModel, ConstituencyTreeSGDClassifierModel
from ExternalData.Models.root_model import RootSGDClassifierModel, RootMLPClassifierModel, RootKNNClassifier, \
    RootRidgeClassifierModel, RootLogisticRegressionClassifier, RootSVMClassifier
from ExternalData.Models.teamim_model import TeamimSVMClassifier, TeamimSGDClassifierModel, TeamimMLPClassifierModel, \
    TeamimKNNClassifier, TeamimRidgeClassifierModel, TeamimLogisticRegressionClassifier
from ExternalData.Models.teamim_tree_model import TeamimTreeSGDClassifierModel, TeamimTreeMLPClassifierModel, \
    TeamimTreeKNNClassifier, TeamimTreeSVMClassifier, TeamimTreeLogisticRegressionClassifier, \
    TeamimTreeRidgeClassifierModel
from ExternalData.Models.text_model import TextSVMClassifier, TextRidgeClassifierModel, TextKNNClassifier, \
    TextLogisticRegressionClassifier, TextMLPClassifierModel, TextSGDClassifierModel


def main():
    # t = Torah()
    # t.read("ExternalData/torah_update.xlsx")
    # t.parse_trees()
    # t.save()
    #
    t2 = Torah()
    t2.load()
    #
    Classifier1 = TeamimTreeSVMClassifier(t2, isBook=False)
    Classifier1.train()
    Classifier1.test()

    # Classifier2 = TeamimTreeLogisticRegressionClassifier(t2, isBook=False)
    # Classifier2.cross_validate()
    #
    # Classifier3 = TeamimTreeRidgeClassifierModel(t2, isBook=False)
    # Classifier3.cross_validate()
    #
    # Classifier4 = TeamimTreeKNNClassifier(t2, n_neighbors=1, isBook=False)
    # Classifier4.cross_validate()
    #
    # Classifier4 = TeamimTreeKNNClassifier(t2, n_neighbors=2, isBook=False)
    # Classifier4.cross_validate()
    #
    # Classifier4 = TeamimTreeKNNClassifier(t2, n_neighbors=3, isBook=False)
    # Classifier4.cross_validate()
    #
    # Classifier4 = TeamimTreeKNNClassifier(t2, n_neighbors=10, isBook=False)
    # Classifier4.cross_validate()
    #
    # Classifier5 = TeamimTreeMLPClassifierModel(t2, isBook=False)
    # Classifier5.cross_validate()
    #
    # Classifier6 = TeamimTreeSGDClassifierModel(t2, isBook=False)
    # Classifier6.cross_validate()




if __name__ == "__main__":
    main()
