import numpy as np
from typing import Any


class RPA:
    def __init__(self, n_iter: int = 10):
        """
        Constructor for the Random Projection Augmentation (RPA) class.

        Parameters:
        n_iter (int): Number of iterations to perform random projection augmentation.

        Returns:
        None
        """
        self.n_iter = n_iter

    def augment(self, X1: np.ndarray, X2: np.ndarray, model) -> Any:
        """
        Perform random projection augmentation.

        Parameters:
        X1 (np.ndarray): The first dataset.
        X2 (np.ndarray): The second dataset.
        model: The model to use for random projection augmentation.

        Returns:
        The augmented model.
        """
        for _ in range(self.n_iter):
            projected_X1, projected_X2 = model.transform(X1, X2)

            X1 = np.concatenate([X1, projected_X1], axis=1)
            X2 = np.concatenate([X2, projected_X2], axis=1)

            model.fit(X1, X2)

        return model
