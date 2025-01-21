from Classes.Torah import Torah
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.feature_extraction.text import CountVectorizer
from abc import ABC, abstractmethod
import numpy as np

symbols = ['72', '92', '85', '74+05', '71+73', '74+80', '94', '84', '82', '04', '63+71', '10', '70', '61', '74', '63+80', '98', '63', '63+71+05', '14+62', '70+73', '93', '62', '02', '73+92', '80', '71+05', '03', '00', '01', '05', '70+05', '71', '74+74', '81', '65+05', '63+05', '94+05', '63+61', '91', '83', '74+81', '14', '73', '63+70', '74+83', '73+00', '12+44', '11']
n = len(symbols)
symbol_permutation = np.random.permutation(range(1, n + 1))
SYMBOL_INDICES = {symbol: str(index) for symbol, index in zip(symbols, symbol_permutation)}
SYMBOL_INDICES.update({"-": '0'})


def symbols_map(symbols):
    return [SYMBOL_INDICES[symbol] for symbol in symbols]

# Base Classifier
class TeamimAndTeamimTreeClassifier(ABC):
    def __init__(self, torah: Torah, pickle_file="torah.pkl", test_size=0.2, random_state=42, isBook=True):
        self.torah = torah
        torah.load(pickle_file)
        self.books = torah.books

        texts, labels = [], []

        if isBook:
            for book in self.books:
                for pasuk in book.psukim:
                    # Extract teamim (symbols) as string
                    teamim = " ".join(symbols_map(pasuk.teamim_tree.root.symbols))

                    # Extract tree features as string (assumed that extract_tree_features is defined)
                    tree_teamim = self.extract_tree_features(pasuk.teamim_tree)
                    tree_teamim_str = " ".join(tree_teamim)

                    # Combine teamim and tree features
                    combined_features = teamim + " " + tree_teamim_str

                    texts.append(combined_features)
                    labels.append(book.book_number)  # Or teuda_name if using Teuda instead of Book
        else:
            for teuda in torah.teudot:
                for pasuk in teuda.psukim:
                    # Extract teamim (symbols) as string
                    teamim = " ".join(symbols_map(pasuk.teamim_tree.root.symbols))

                    # Extract tree features as string (assumed that extract_tree_features is defined)
                    tree = pasuk.constituency_tree
                    tree_features = self.extract_tree_features(tree)
                    tree_features_str = " ".join(tree_features)

                    # Combine teamim and tree features
                    combined_features = teamim + " " + tree_features_str

                    texts.append(combined_features)
                    labels.append(teuda.teuda_name)

        # Vectorize the texts
        cv = CountVectorizer()

        # Perform train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state
        )

        # Fit the vectorizer to training data
        self.X_train = cv.fit_transform(self.X_train)
        self.X_test = cv.transform(self.X_test)

        # Model initialization
        self.model = None
        self.model_name = None
        self.isBook = isBook

    def extract_tree_features(self, teamim_tree):
        features = [teamim_tree.to_vector(), str(teamim_tree.height()), str(teamim_tree.size())]
        return features

    @abstractmethod
    def initialize_model(self):
        """Initialize the specific model. To be implemented by subclasses."""
        pass


    def train(self):
        if self.model is None:
            self.initialize_model()

        self.model.fit(self.X_train, self.y_train)
        print(f"{self.model_name} training completed.")

    def test(self):
        if self.model is None:
            raise ValueError("Model is not initialized or trained.")

        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"{self.model_name} Accuracy: {accuracy:.4f}")

        precision = precision_score(self.y_test, y_pred, average='weighted')
        recall = recall_score(self.y_test, y_pred, average='weighted')
        f1 = f1_score(self.y_test, y_pred, average='weighted')

        print(f"{self.model_name} Precision: {precision:.4f}")
        print(f"{self.model_name} Recall: {recall:.4f}")
        print(f"{self.model_name} F1 Score: {f1:.4f}")

        if self.isBook:
            report = classification_report(self.y_test, y_pred,
                                           target_names=[f"Book {book.book_name}" for book in self.torah.books])
        else:
            report = classification_report(self.y_test, y_pred,
                                           target_names=[f"Teuda {teuda.teuda_name}" for teuda in self.torah.teudot])
        print(report)

    def cross_validate(self, cv_folds=10):
        if self.model is None:
            self.initialize_model()

        kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        cross_val_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=kf, scoring='accuracy')
        print(f"{self.model_name} Average cross-validation score: {np.mean(cross_val_scores):.4f}")

# Subclasses for Specific Models
class TeamimAndTeamimTreeLogisticRegressionClassifier(TeamimAndTeamimTreeClassifier):
    def initialize_model(self):
        self.model = LogisticRegression(max_iter = 500)
        self.model_name = "Logistic Regression"


class TeamimAndTeamimTreeRidgeClassifierModel(TeamimAndTeamimTreeClassifier):
    def initialize_model(self):
        self.model = RidgeClassifier()
        self.model_name = "Ridge Classifier"


class TeamimAndTeamimTreeSVMClassifier(TeamimAndTeamimTreeClassifier):
    def initialize_model(self):
        self.model = SVC(kernel = "linear")
        self.model_name = "SVM"


class TeamimAndTeamimTreeKNNClassifier(TeamimAndTeamimTreeClassifier):
    def __init__(self, torah : Torah, pickle_file = "torah.pkl", test_size = 0.2, random_state = 42, isBook = True, n_neighbors = 10):
        super(TeamimAndTeamimTreeKNNClassifier, self).__init__(torah, pickle_file, test_size, random_state, isBook)
        self.n_neighbors = n_neighbors

    def initialize_model(self):
        self.model = KNeighborsClassifier(n_neighbors = self.n_neighbors)
        self.model_name = f"K-NN (k={self.n_neighbors})"


class TeamimAndTeamimTreeMLPClassifierModel(TeamimAndTeamimTreeClassifier):
    def initialize_model(self):
        self.model = MLPClassifier(max_iter = 1000)
        self.model_name = "MLP Classifier"


class TeamimAndTeamimTreeSGDClassifierModel(TeamimAndTeamimTreeClassifier):
    def initialize_model(self):
        self.model = SGDClassifier(max_iter = 1000)
        self.model_name = "SGD Classifier"