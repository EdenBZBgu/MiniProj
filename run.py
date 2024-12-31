from Classes.Torah import Torah
from ExternalData.statistics import calculate_word_frequencies_by_book, calculate_word_frequencies_by_teuda, \
    calculate_phraseText_frequencies_byBook, calculate_pasuk_lengths_by_book, calculate_unique_word_counts_by_book, \
    calculate_tree_depths


def main():

    # t = Torah()
    # t.read("ExternalData/torah_update.xlsx")
    # t.parse_trees()
    # t.save()

    t2 = Torah()
    t2.load()

    word_counter = calculate_tree_depths(t2)
    print(word_counter)



if __name__ == "__main__":
    main()
