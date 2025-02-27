from Classes.Torah import Torah
from ExternalData.Models.W_C_CTree_model import WCharacteristicTreeSVMClassifier, \
    WCharacteristicTreeRidgeClassifierModel, WCharacteristicTreeKNNClassifier, \
    WCharacteristicTreeLogisticRegressionClassifier, WCharacteristicTreeMLPClassifierModel, \
    WCharacteristicTreeSGDClassifierModel
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
    TeamimKNNClassifier, TeamimRidgeClassifierModel, ConstituencyTreeLogisticRegressionClassifier
from ExternalData.Models.teamim_treeTeamim_model import TeamimAndTeamimTreeSVMClassifier, \
    TeamimAndTeamimTreeLogisticRegressionClassifier, TeamimAndTeamimTreeRidgeClassifierModel, \
    TeamimAndTeamimTreeKNNClassifier, TeamimAndTeamimTreeMLPClassifierModel, TeamimAndTeamimTreeSGDClassifierModel
from ExternalData.Models.teamim_tree_model import TeamimTreeSGDClassifierModel, TeamimTreeMLPClassifierModel, \
    TeamimTreeKNNClassifier, TeamimTreeSVMClassifier, TeamimTreeLogisticRegressionClassifier, \
    TeamimTreeRidgeClassifierModel
from ExternalData.Models.text_model import TextSVMClassifier, TextRidgeClassifierModel, TextKNNClassifier, \
    TextLogisticRegressionClassifier, TextMLPClassifierModel, TextSGDClassifierModel
from ExternalData.Statistics.statistics import calculate_word_frequencies_by_book, calculate_word_frequencies_by_teuda, \
    calculate_phraseText_frequencies_by_Book, calculate_pasuk_lengths_by_book, calculate_pasuk_lengths_by_teuda, \
    calculate_psukim_by_teuda_and_book


def main():
    # t = Torah()
    # t.read("ExternalData/torah_update.xlsx")
    # t.parse_trees()
    # t.save()
    #
    t2 = Torah()
    t2.load()
    #
    # model1 = WCharacteristicTreeLogisticRegressionClassifier(t2, isBook=False)
    # model1.cross_validate()
    #
    # model2 = WCharacteristicTreeRidgeClassifierModel(t2, isBook=False)
    # model2.cross_validate()
    #
    # model3 = WCharacteristicTreeSVMClassifier(t2, isBook=False)
    # model3.cross_validate()
    #
    # model4 = WCharacteristicTreeKNNClassifier(t2, isBook=False, n_neighbors=1)
    # model4.cross_validate()
    #
    # model5 = WCharacteristicTreeKNNClassifier(t2, isBook=False, n_neighbors=2)
    # model5.cross_validate()
    #
    # model6 = WCharacteristicTreeKNNClassifier(t2, isBook=False,n_neighbors=3)
    # model6.cross_validate()
    #
    # model7 = WCharacteristicTreeKNNClassifier(t2, isBook=False, n_neighbors=10)
    # model7.cross_validate()

    model8 = WCharacteristicTreeMLPClassifierModel(t2, isBook=False)
    model8.train()
    model8.test()

    # model9 = WCharacteristicTreeSGDClassifierModel(t2, isBook=False)
    # model9.cross_validate()






if __name__ == "__main__":
    main()
