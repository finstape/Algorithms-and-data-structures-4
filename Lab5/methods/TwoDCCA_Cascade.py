import os
import pickle

import numpy as np
from sklearn.cross_decomposition import CCA


class TwoDCCACascade:
    def __init__(self, n_components: int = 1):
        """
        Constructor for TwoDCCACascade class.

        Parameters:
        n_components (int): Number of canonical components to compute and return.

        Returns:
        None
        """
        self.n_components = n_components
        self.cca = CCA(n_components=n_components)

    def fit(self, X_regular: np.ndarray, X_infrared: np.ndarray) -> None:
        """
        Fit the model to the regular and infrared images.

        Parameters:
        X_regular (np.ndarray): Regular images.
        X_infrared (np.ndarray): Infrared images.

        Returns:
        None
        """
        # Reshape input data if necessary
        if X_regular.ndim >= 3:
            X_regular = X_regular.reshape(X_regular.shape[0], -1)
        if X_infrared.ndim >= 3:
            X_infrared = X_infrared.reshape(X_infrared.shape[0], -1)

        # Fit CCA to the data
        self.cca.fit(X_regular, X_infrared)

    def transform(self, X_regular: np.ndarray, X_infrared: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Transform the regular and infrared images.

        Parameters:
        X_regular (np.ndarray): Regular images.
        X_infrared (np.ndarray): Infrared images.

        Returns:
        Tuple of NumPy arrays: Transformed regular and infrared images.
        """
        # Reshape input data if necessary
        if X_regular.ndim >= 3:
            X_regular = X_regular.reshape(X_regular.shape[0], -1)
        if X_infrared.ndim >= 3:
            X_infrared = X_infrared.reshape(X_infrared.shape[0], -1)

        # Transform data using the fitted CCA model
        transformed_regular, transformed_infrared = self.cca.transform(X_regular, X_infrared)

        return transformed_regular, transformed_infrared

    def train(self, X_regular: np.ndarray, X_infrared: np.ndarray) -> None:
        """
        Train the CCA model on regular and infrared images.

        Parameters:
        X_regular (np.ndarray): Regular images.
        X_infrared (np.ndarray): Infrared images.

        Returns:
        None
        """
        self.fit(X_regular, X_infrared)

    def save_model(self, output_folder: str) -> None:
        """
        Save the trained CCA model.

        Parameters:
        output_folder (str): Path to the folder where the model will be saved.

        Returns:
        None
        """
        # Check if the output folder exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the trained CCA model
        model_filename = os.path.join(output_folder, "cca_model.pkl")
        with open(model_filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(model_file: str) -> 'TwoDCCACascade':
        """
        Load a saved CCA model.

        Parameters:
        model_file (str): Path to the saved model file.

        Returns:
        TwoDCCACascade: Loaded CCA model.
        """
        with open(model_file, 'rb') as f:
            return pickle.load(f)
