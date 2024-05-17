import pickle
from typing import Any
import numpy as np
from numpy import ndarray


class TwoDCCAParallel:
    def __init__(self, dimension: int = 10, distance_function=lambda x, y: np.linalg.norm(x - y), is_max: bool = True):
        """
        Initializes a new instance of the Parallel Two-Dimensional Canonical Correlation Analysis (2DCCA) class.

        Parameters:
        dimension (int): The dimension of the canonical correlation space. Default is 10.
        distance_function (function): The distance function used to measure the similarity between samples.
                                      Default is the Euclidean distance function.
        is_max (bool): Determines whether to maximize or minimize the canonical correlation. Default is True (maximize).
        """
        self.dimension = dimension
        self.distance_function = distance_function
        self.is_max = is_max

        self.X1 = None
        self.X2 = None
        self.W1 = None
        self.W2 = None

    def fit(self, X1: np.ndarray, X2: np.ndarray) -> None:
        """
        Fit the Parallel 2DCCA model to the given data.

        Parameters:
        X1 (np.ndarray): The first dataset.
        X2 (np.ndarray): The second dataset.

        Returns:
        None
        """
        assert X1.shape[0] == X2.shape[0], "The number of samples in X1 and X2 must be equal"
        self.X1 = X1.reshape(X1.shape[0], -1)
        self.X2 = X2.reshape(X2.shape[0], -1)

        # Compute the covariance matrices
        C1 = np.cov(self.X1.T)
        C2 = np.cov(self.X2.T)

        # Compute the cross-covariance matrix
        C12 = np.cov(self.X1.T, self.X2.T)[:self.X1.shape[1], self.X1.shape[1]:]

        # Compute the eigenvalues and eigenvectors of C1^(-1/2) C12 C2^(-1/2)
        S = np.linalg.inv(np.sqrt(np.diag(np.diag(C1)))) @ C12 @ np.linalg.inv(np.sqrt(np.diag(np.diag(C2))))
        eigenvalues, eigenvectors = np.linalg.eig(S)

        # Sort eigenvectors based on eigenvalues
        sorted_indices = np.argsort(eigenvalues.real)[::-1]
        self.W1 = eigenvectors.real[:, sorted_indices[:self.dimension]]
        self.W2 = eigenvectors.real[:, sorted_indices[:self.dimension]]

    def transform(self, X1: np.ndarray, X2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Transform the given data using the fitted model.

        Parameters:
        X1 (np.ndarray): The first dataset to transform.
        X2 (np.ndarray): The second dataset to transform.

        Returns:
        tuple[np.ndarray, np.ndarray]: Transformed datasets.
        """
        return X1 @ self.W1, X2 @ self.W2

    def predict(self, X1_new: np.ndarray, X2_new: np.ndarray) -> list[tuple[ndarray, ndarray, Any]]:
        """
        Predict the output for the given input data using the fitted model.

        Parameters:
        X1_new (np.ndarray): The new data for the first dataset.
        X2_new (np.ndarray): The new data for the second dataset.

        Returns:
        list[tuple[int, float]]: Predicted output.
        """
        transformed_X1_new, transformed_X2_new = self.transform(X1_new, X2_new)
        distances = np.zeros((X1_new.shape[0], X2_new.shape[0]))

        for i, x1_new in enumerate(transformed_X1_new):
            for j, x2_new in enumerate(transformed_X2_new):
                distances[i, j] = self.distance_function(x1_new, x2_new)

        if self.is_max:
            indices = np.unravel_index(np.argmax(distances), distances.shape)
        else:
            indices = np.unravel_index(np.argmin(distances), distances.shape)

        return [(indices[0], indices[1], distances[indices])]

    def train(self, X1: np.ndarray, X2: np.ndarray) -> None:
        """
        Train the Parallel 2DCCA model on the given data.

        Parameters:
        X1 (np.ndarray): The first dataset.
        X2 (np.ndarray): The second dataset.

        Returns:
        None
        """
        self.fit(X1, X2)

    def save_model(self, output_file: str) -> None:
        """
        Save the trained model to a file.

        Parameters:
        output_file (str): Path to the file where the model will be saved.

        Returns:
        None
        """
        with open(output_file, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(model_file: str) -> 'TwoDCCAParallel':
        """
        Load a trained model from a file.

        Parameters:
        model_file (str): Path to the file containing the saved model.

        Returns:
        TwoDCCAParallel: Loaded model.
        """
        with open(model_file, 'rb') as f:
            return pickle.load(f)
