import pandas as pd
from collections import Counter
from Classes.Torah  import Torah

def calculate_word_frequencies_by_book(tora: Torah):
    """
    Count the frequencies of all words in each book separately.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with word frequencies.
    """
    book_word_frequencies = {}

    for book in tora.books:
        word_counter = Counter()

        # Count words in the current book
        for pasuk in book.psukim:
            word_counter.update(pasuk.words())

        # Convert the Counter to a Pandas DataFrame
        word_df = pd.DataFrame.from_dict(word_counter, orient="index", columns=["Frequency"])
        word_df.index.name = "Word"
        word_df = word_df.sort_values(by="Frequency", ascending=False)

        # Store the DataFrame in the dictionary using the book name as the key
        book_word_frequencies[book.book_name] = word_df
        word_check = word_df["Frequency"].isna().sum()
    return book_word_frequencies

def calculate_word_frequencies_by_teuda(tora: Torah):
    """
    Count the frequencies of all words in each teuda separately.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with word frequencies.
    """
    teuda_word_frequencies = {}

    for teuda in tora.teudot:
        word_counter = Counter()

        # Count words in the current book
        for pasuk in teuda.psukim:
            word_counter.update(pasuk.words())

        # Convert the Counter to a Pandas DataFrame
        word_df = pd.DataFrame.from_dict(word_counter, orient="index", columns=["Frequency"])
        word_df.index.name = "Word"
        word_df = word_df.sort_values(by="Frequency", ascending=False)

        # Store the DataFrame in the dictionary using the book name as the key
        teuda_word_frequencies[teuda.teuda_name] = word_df

    return teuda_word_frequencies

def calculate_pasuk_lengths_by_book(tora: Torah):
    """
    Calculate the lengths (number of words) of psukim for each book separately.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with pasuk lengths.
    """
    dp_table_data = []
    book_pasuk_lengths = {}

    for book in tora.books:
        # Create a list to store pasuk data for the current book
        pasuk_data = []

        for pasuk in book.psukim:
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Pasuk Length": pasuk._word_count,
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the book name as the key
        book_pasuk_lengths[book.book_name] = pasuk_df

        # Calculate statistics for the current book

        min_length = pasuk_df["Pasuk Length"].min()
        max_length = pasuk_df["Pasuk Length"].max()
        avg_length = pasuk_df["Pasuk Length"].mean()

        dp_table_data.append({
            "Book": book.book_name,
            "Min Length": min_length,
            "Max Length": max_length,
            "Average Length": avg_length
        })

    book_df = pd.DataFrame(dp_table_data)

    return book_pasuk_lengths, book_df

def calculate_pasuk_lengths_by_teuda(tora: Torah):
    """
    Calculate the lengths (number of words) of psukim for each teuda separately.
    :return: A dictionary where keys are teuda names and values are Pandas DataFrames with pasuk lengths.
    """
    dp_table_data = []
    teuda_pasuk_lengths = {}

    for teuda in tora.teudot:
        # Create a list to store pasuk data for the current teuda
        pasuk_data = []

        for pasuk in teuda.psukim:
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Pasuk Length": pasuk._word_count,
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the book name as the key
        teuda_pasuk_lengths[teuda.teuda_name] = pasuk_df

        # Calculate statistics for the current book

        min_length = pasuk_df["Pasuk Length"].min()
        max_length = pasuk_df["Pasuk Length"].max()
        avg_length = pasuk_df["Pasuk Length"].mean()

        dp_table_data.append({
            "teuda": teuda.teuda_name,
            "Min Length": min_length,
            "Max Length": max_length,
            "Average Length": avg_length
        })

    teuda_df = pd.DataFrame(dp_table_data)

    return teuda_pasuk_lengths, teuda_df

def calculate_unique_word_counts_by_book(tora: Torah):
    """
    Calculate the number of unique words for each pasuk in each book manually.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with unique word counts.
    """
    book_unique_word_counts = {}

    for book in tora.books:
        # Create a list to store pasuk data for the current book
        pasuk_data = []

        for pasuk in book.psukim:
            # Calculate unique words manually
            unique_words = set(pasuk._words)  # Convert the list of words to a set for uniqueness
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Unique Word Count": len(unique_words),
                "Total Words": len(pasuk._words),  # Total words in the pasuk
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the book name as the key
        book_unique_word_counts[book.book_name] = pasuk_df

    return book_unique_word_counts

def calculate_unique_word_counts_by_teuda(tora: Torah):
    """
    Calculate the number of unique words for each pasuk in each teuda manually.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with unique word counts.
    """
    teuda_unique_word_counts = {}

    for teuda in tora.teudot:
        # Create a list to store pasuk data for the current teuda
        pasuk_data = []

        for pasuk in teuda.psukim:
            # Calculate unique words manually
            unique_words = set(pasuk._words)  # Convert the list of words to a set for uniqueness
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Unique Word Count": len(unique_words),
                "Total Words": len(pasuk._words),  # Total words in the pasuk
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the teuda name as the key
        teuda_unique_word_counts[teuda.teuda_name] = pasuk_df

    return teuda_unique_word_counts

def calculate_tree_depths_by_book(tora: Torah):
    """
    Calculate the depth of the three trees (teamim_tree, constituency_tree, dependency_tree)
    for each pasuk in each book.

    :return: A dictionary where keys are book names and values are Pandas DataFrames with tree depths.
    """
    book_tree_depths = {}

    for book in tora.books:
        # Create a list to store pasuk data for the current book
        pasuk_data = []

        for pasuk in book.psukim:
            # Initialize tree depths as None (if the tree doesn't exist)
            teamim_tree_depth = None
            constituency_tree_depth = None
            dependency_tree_depth = None

            # Calculate tree depths if the respective tree exists
            if pasuk.teamim_tree:
                teamim_tree_depth = pasuk.teamim_tree.height()
            if pasuk.constituency_tree:
                constituency_tree_depth = pasuk.constituency_tree.height()
            if pasuk.dependency_tree:
                dependency_tree_depth = pasuk.dependency_tree.height()

            # Append data for this pasuk
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Teamim Tree Depth": teamim_tree_depth,
                "Constituency Tree Depth": constituency_tree_depth,
                "Dependency Tree Depth": dependency_tree_depth,
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the book name as the key
        book_tree_depths[book.book_name] = pasuk_df

    return book_tree_depths

def calculate_tree_depths_by_teuda(tora: Torah):
    """
    Calculate the depth of the three trees (teamim_tree, constituency_tree, dependency_tree)
    for each pasuk in each teuda.

    :return: A dictionary where keys are teuda names and values are Pandas DataFrames with tree depths.
    """
    teuda_tree_depths = {}

    for teuda in tora.teudot:
        # Create a list to store pasuk data for the current teuda
        pasuk_data = []

        for pasuk in teuda.psukim:
            # Initialize tree depths as None (if the tree doesn't exist)
            teamim_tree_depth = None
            constituency_tree_depth = None
            dependency_tree_depth = None

            # Calculate tree depths if the respective tree exists
            if pasuk.teamim_tree:
                teamim_tree_depth = pasuk.teamim_tree.height()
            if pasuk.constituency_tree:
                constituency_tree_depth = pasuk.constituency_tree.height()
            if pasuk.dependency_tree:
                dependency_tree_depth = pasuk.dependency_tree.height()

            # Append data for this pasuk
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Teamim Tree Depth": teamim_tree_depth,
                "Constituency Tree Depth": constituency_tree_depth,
                "Dependency Tree Depth": dependency_tree_depth,
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the teuda name as the key
        teuda_tree_depths[teuda.teuda_name] = pasuk_df

    return teuda_tree_depths

def calculate_phrases_per_pasuk_constituency(tora: Torah):
    """
    Calculate the number of the phrases in constituency tree for each pasuk in each book.

    :return: A dictionary where keys are book names and values are Pandas DataFrames with tree number of phrases.
    """
    book_tree_num_of_phrase = {}

    for book in tora.books:
        # Create a list to store pasuk data for the current book
        pasuk_data = []

        for pasuk in book.psukim:
            #  Calculate number of phrases
            constituency_tree_phrases = len(pasuk.constituency_tree.psukiot)

            # Append data for this pasuk
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Number of phrases by constituency tree": constituency_tree_phrases
            })

        # Convert the list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the book name as the key
        book_tree_num_of_phrase[book.book_name] = pasuk_df

    return book_tree_num_of_phrase

def encode_tree_patterns_by_book(tora: Torah):
    """
    Encode tree size patterns for each pasuk in each book.

    :param tora: Torah object containing books, where each book has psukim with tree structures.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with tree sizes.
    """
    book_tree_sizes = {}

    for book in tora.books:
        pasuk_data = []

        for pasuk in book.psukim:
            # Initialize tree sizes as None in case they don't exist
            teamim_tree_size = None
            constituency_tree_size = None
            dependency_tree_size = None

            # Compute tree sizes if the tree exists
            if pasuk.teamim_tree:
                teamim_tree_size = pasuk.teamim_tree.size()
            if pasuk.constituency_tree:
                constituency_tree_size = pasuk.constituency_tree.size()
            if pasuk.dependency_tree:
                dependency_tree_size = pasuk.dependency_tree.size()

            # Store data for this pasuk
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Teamim Tree Size": teamim_tree_size,
                "Constituency Tree Size": constituency_tree_size,
                "Dependency Tree Size": dependency_tree_size,
            })

        # Convert list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the book name as the key
        book_tree_sizes[book.book_name] = pasuk_df

    return book_tree_sizes

def encode_tree_patterns_by_teuda(tora: Torah):
    """
    Encode tree size patterns for each pasuk in each teuda.

    :param tora: Torah object containing teudot, where each teuda has psukim with tree structures.
    :return: A dictionary where keys are teuda names and values are Pandas DataFrames with tree sizes.
    """
    teuda_tree_sizes = {}

    for teuda in tora.teudot:
        pasuk_data = []

        for pasuk in teuda.psukim:
            # Initialize tree sizes as None in case they don't exist
            teamim_tree_size = None
            constituency_tree_size = None
            dependency_tree_size = None

            # Compute tree sizes if the tree exists
            if pasuk.teamim_tree:
                teamim_tree_size = pasuk.teamim_tree.size()
            if pasuk.constituency_tree:
                constituency_tree_size = pasuk.constituency_tree.size()
            if pasuk.dependency_tree:
                dependency_tree_size = pasuk.dependency_tree.size()

            # Store data for this pasuk
            pasuk_data.append({
                "Pasuk ID": pasuk._pasuk_id,
                "Teamim Tree Size": teamim_tree_size,
                "Constituency Tree Size": constituency_tree_size,
                "Dependency Tree Size": dependency_tree_size,
            })

        # Convert list of dictionaries to a Pandas DataFrame
        pasuk_df = pd.DataFrame(pasuk_data)

        # Store the DataFrame in the dictionary using the teuda name as the key
        teuda_tree_sizes[teuda.teuda_name] = pasuk_df

    return teuda_tree_sizes

def calculate_top_10_words_by_book(tora: Torah):
    """
    Find the top 10 most frequent words in each book separately.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with the top 10 word frequencies.
    """
    top_10_words_by_book = {}

    for book in tora.books:
        word_counter = Counter()

        # Count words in the current book
        for pasuk in book.psukim:
            word_counter.update(pasuk.words())

        # Convert the Counter to a Pandas DataFrame
        word_df = pd.DataFrame.from_dict(word_counter, orient="index", columns=["Frequency"])
        word_df.index.name = "Word"
        word_df = word_df.sort_values(by="Frequency", ascending=False)

        # Get the top 10 words
        top_10_words_by_book[book.book_name] = word_df.head(10)

    return top_10_words_by_book

def calculate_top_10_words_by_teuda(tora: Torah):
    """
    Find the top 10 most frequent words in each teuda separately.
    :return: A dictionary where keys are book names and values are Pandas DataFrames with the top 10 word frequencies.
    """
    top_10_words_by_teuda = {}

    for teuda in tora.teudot:
        word_counter = Counter()

        # Count words in the current book
        for pasuk in teuda.psukim:
            word_counter.update(pasuk.words())

        # Convert the Counter to a Pandas DataFrame
        word_df = pd.DataFrame.from_dict(word_counter, orient="index", columns=["Frequency"])
        word_df.index.name = "Word"
        word_df = word_df.sort_values(by="Frequency", ascending=False)

        # Get the top 10 words
        top_10_words_by_teuda[teuda.teuda_name] = word_df.head(10)

    return top_10_words_by_teuda

def calculate_average_word_length_by_book(tora: Torah):
    """
    Calculate the average word length in each book separately.
    :return: A dictionary where keys are book names and values are the average word length (float).
    """
    average_word_lengths = {}

    for book in tora.books:
        total_word_length = 0
        total_word_count = 0

        # Calculate total word length and word count in the current book
        for pasuk in book.psukim:
            words = pasuk.words()
            total_word_length += sum(len(word) for word in words)
            total_word_count += len(words)

        # Calculate the average word length
        if total_word_count > 0:
            average_word_lengths[book.book_name] = total_word_length / total_word_count
        else:
            average_word_lengths[book.book_name] = 0

    return average_word_lengths

def calculate_average_word_length_by_teuda(tora: Torah):
    """
    Calculate the average word length in each teuda separately.
    :return: A dictionary where keys are teuda names and values are the average word length (float).
    """
    average_word_lengths = {}

    for teuda in tora.teudot:
        total_word_length = 0
        total_word_count = 0

        # Calculate total word length and word count in the current teuda
        for pasuk in teuda.psukim:
            words = pasuk.words()
            total_word_length += sum(len(word) for word in words)
            total_word_count += len(words)

        # Calculate the average word length
        if total_word_count > 0:
            average_word_lengths[teuda.teuda_name] = total_word_length / total_word_count
        else:
            average_word_lengths[teuda.teuda_name] = 0

    return average_word_lengths

def calculate_psukim_by_teuda_and_book(tora: Torah):
    """
    Count how many psukim in each book belong to each teuda.
    :return: A nested dictionary where the first key is the book name, the second key is the teuda name (str),
             and the value is the count of psukim belonging to that teuda in that book.
    """
    psukim_by_teuda_and_book = {}

    for book in tora.books:
        # Initialize a dictionary to store the counts for each teuda in the current book
        teuda_counter = {}

        for pasuk in book.psukim:
            # Each pasuk has a `teuda_name` attribute as a string
            teuda_name = pasuk.teuda

            # Increment the counter for the corresponding teuda
            if teuda_name not in teuda_counter:
                teuda_counter[teuda_name] = 0
            teuda_counter[teuda_name] += 1

        # Store the counts dictionary under the book name
        psukim_by_teuda_and_book[book.book_name] = teuda_counter

    return psukim_by_teuda_and_book

