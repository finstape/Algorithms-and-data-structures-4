from sklearn.cross_decomposition import PLSRegression
import numpy as np


class PLSCascade:
    def __init__(self, n_components: int = 2, n_cascades: int = 3):
        """
        Constructor for the PLS Cascade class.

        Parameters:
        n_components (int): Number of components to keep.
        n_cascades (int): Number of cascades to perform.

        Returns:
        None
        """
        self.n_components = n_components
        self.n_cascades = n_cascades
        self.pls_models = []

    def fit(self, X1: np.ndarray, X2: np.ndarray):
        """
        Fit the PLS cascade model to the data.

        Parameters:
        X1 (np.ndarray): First dataset.
        X2 (np.ndarray): Second dataset.
        """
        for _ in range(self.n_cascades):
            pls = PLSRegression(n_components=self.n_components)
            pls.fit(X1, X2)
            self.pls_models.append(pls)
            X1, X2 = pls.transform(X1, X2)

    def transform(self, X1: np.ndarray, X2: np.ndarray):
        """
        Transform the input data using the PLS cascade model.

        Parameters:
        X1 (np.ndarray): First dataset.
        X2 (np.ndarray): Second dataset.

        Returns:
        tuple: Transformed datasets.
        """
        for pls in self.pls_models:
            X1, X2 = pls.transform(X1, X2)
        return X1, X2

    def predict(self, X1: np.ndarray, X2: np.ndarray):
        """
        Predict using the PLS cascade model.

        Parameters:
        X1 (np.ndarray): First dataset.
        X2 (np.ndarray): Second dataset.

        Returns:
        tuple: Predicted values for both datasets.
        """
        return self.transform(X1, X2)
