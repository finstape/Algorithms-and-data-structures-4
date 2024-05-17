from sklearn.cross_decomposition import PLSRegression
import numpy as np
from concurrent.futures import ThreadPoolExecutor


class PLSParallel:
    def __init__(self, n_components: int = 2, n_jobs: int = -1):
        """
        Constructor for the PLS Parallel class.

        Parameters:
        n_components (int): Number of components to keep.
        n_jobs (int): Number of parallel jobs to run. Default is -1.

        Returns:
        None
        """
        self.pls_models = None
        self.n_components = n_components
        self.n_jobs = n_jobs

    def fit(self, X1: np.ndarray, X2: np.ndarray):
        """
        Fit the PLS parallel model to the data.

        Parameters:
        X1 (np.ndarray): First dataset.
        X2 (np.ndarray): Second dataset.
        """
        self.pls_models = []
        with ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            for _ in range(self.n_components):
                pls = PLSRegression(n_components=1)
                future = executor.submit(pls.fit, X1, X2)
                self.pls_models.append(future.result())
                X1, X2 = pls.transform(X1, X2)

    def transform(self, X1: np.ndarray, X2: np.ndarray):
        """
        Transform the input data using the PLS parallel model.

        Parameters:
        X1 (np.ndarray): First dataset.
        X2 (np.ndarray): Second dataset.

        Returns:
        tuple: Transformed datasets.
        """
        transformed_X1 = np.empty((X1.shape[0], self.n_components))
        transformed_X2 = np.empty((X2.shape[0], self.n_components))

        with ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            for i, pls in enumerate(self.pls_models):
                transformed_X1[:, i], transformed_X2[:, i] = executor.submit(pls.transform, X1, X2)

        return transformed_X1, transformed_X2

    def predict(self, X1: np.ndarray, X2: np.ndarray):
        """
        Predict using the PLS parallel model.

        Parameters:
        X1 (np.ndarray): First dataset.
        X2 (np.ndarray): Second dataset.

        Returns:
        tuple: Predicted values for both datasets.
        """
        return self.transform(X1, X2)
