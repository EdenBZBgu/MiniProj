from Classes.Torah import Torah
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.feature_extraction.text import CountVectorizer
from abc import ABC, abstractmethod
import numpy as np


# Base Classifier
class ConstituencyTreeClassifier(ABC):
    def __init__(self, torah : Torah, pickle_file = "torah.pkl", test_size = 0.2, random_state = 42, isBook = True):
        self.torah = torah
        torah.load(pickle_file)
        self.books = torah.books

        texts, labels = [], []
        if (isBook):
            for book in self.books:
                for pasuk in book.psukim:
                    tree = pasuk.constituency_tree
                    features = self.extract_tree_features(tree)
                    featuresStr = " ".join(features)
                    texts.append(featuresStr)
                    labels.append(book.book_number)
        else:
            for teuda in torah.teudot:
                for pasuk in teuda.psukim:
                    tree = pasuk.constituency_tree
                    features = self.extract_tree_features(tree)
                    featuresStr = " ".join(features)
                    texts.append(featuresStr)
                    labels.append(teuda.teuda_name)

        cv = CountVectorizer()
        # Perform train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            texts, labels, test_size = test_size, random_state = random_state
        )
        self.X_train = cv.fit_transform(self.X_train)
        self.X_test = cv.transform(self.X_test)

        self.model = None
        self.model_name = None

    def extract_tree_features(self, constituency_tree):
        features = []
        features.append(constituency_tree.to_vector())
        features.append(str(constituency_tree.height()))
        features.append(str(constituency_tree.size()))
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

    def cross_validate(self, cv_folds=10):
        if self.model is None:
            self.initialize_model()

        kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        cross_val_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=kf, scoring='accuracy')
        print(f"{self.model_name} Average cross-validation score: {np.mean(cross_val_scores):.4f}")

# Subclasses for Specific Models
class ConstituencyTreeLogisticRegressionClassifier(ConstituencyTreeClassifier):
    def initialize_model(self):
        self.model = LogisticRegression(max_iter = 500)
        self.model_name = "Logistic Regression"


class ConstituencyTreeRidgeClassifierModel(ConstituencyTreeClassifier):
    def initialize_model(self):
        self.model = RidgeClassifier()
        self.model_name = "Ridge Classifier"


class ConstituencyTreeSVMClassifier(ConstituencyTreeClassifier):
    def initialize_model(self):
        self.model = SVC(kernel = "linear")
        self.model_name = "SVM"


class ConstituencyTreeKNNClassifier(ConstituencyTreeClassifier):
    def __init__(self, torah : Torah, pickle_file = "torah.pkl", test_size = 0.2, random_state = 42, isBook = True, n_neighbors = 10):
        super(ConstituencyTreeKNNClassifier, self).__init__(torah, pickle_file, test_size, random_state, isBook)
        self.n_neighbors = n_neighbors

    def initialize_model(self):
        self.model = KNeighborsClassifier(n_neighbors = self.n_neighbors)
        self.model_name = f"K-NN (k={self.n_neighbors})"


class ConstituencyTreeMLPClassifierModel(ConstituencyTreeClassifier):
    def initialize_model(self):
        self.model = MLPClassifier(max_iter = 1000)
        self.model_name = "MLP Classifier"


class ConstituencyTreeSGDClassifierModel(ConstituencyTreeClassifier):
    def initialize_model(self):
        self.model = SGDClassifier(max_iter = 1000)
        self.model_name = "SGD Classifier"