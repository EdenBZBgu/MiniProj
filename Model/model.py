from Classes.Torah import Torah
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from abc import ABC, abstractmethod


# Base Classifier
class Classifier(ABC):
    def __init__(self, torah : Torah, pickle_file = "torah_dmp.pkl", test_size = 0.2, random_state = 42):
        self.torah = torah
        torah.load(pickle_file)
        self.books = torah.books

        texts, labels = [], []
        for book in self.books:
            for pasuk in book.psukim:
                texts.append(pasuk.text)
                labels.append(book.book_number)

        # Perform train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            texts, labels, test_size = test_size, random_state = random_state
        )

        self.model = None
        self.model_name = None

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


# Subclasses for Specific Models
class LogisticRegressionClassifier(Classifier):
    def initialize_model(self):
        self.model = LogisticRegression(max_iter = 500)
        self.model_name = "Logistic Regression"


class RidgeClassifierModel(Classifier):
    def initialize_model(self):
        self.model = RidgeClassifier()
        self.model_name = "Ridge Classifier"


class SVMClassifier(Classifier):
    def initialize_model(self):
        self.model = SVC(kernel = "linear")
        self.model_name = "SVM"


class KNNClassifier(Classifier):
    def __init__(self, texts, labels, n_neighbors, **kwargs):
        super().__init__(texts, labels, **kwargs)
        self.n_neighbors = n_neighbors

    def initialize_model(self):
        self.model = KNeighborsClassifier(n_neighbors = self.n_neighbors)
        self.model_name = f"K-NN (k={self.n_neighbors})"


class MLPClassifierModel(Classifier):
    def initialize_model(self):
        self.model = MLPClassifier(max_iter = 1000)
        self.model_name = "MLP Classifier"


class SGDClassifierModel(Classifier):
    def initialize_model(self):
        self.model = SGDClassifier(max_iter = 1000)
        self.model_name = "SGD Classifier"

