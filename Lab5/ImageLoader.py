import numpy as np
import cv2
import os


class ImageLoader:
    def __init__(self, path: str):
        """
        Constructor for ImageLoader class

        Parameters:
        path (str): Path to the images

        Returns:
        None
        """
        self.path = path

    @staticmethod
    def sharpen_image(image: np.ndarray) -> np.ndarray:
        """
        Sharpen the image.

        Parameters:
        image (np.ndarray): Input image.

        Returns:
        np.ndarray: Sharpened image.
        """
        # Define the sharpening kernel
        sharpen_filter = np.array([[-1, -1, -1],
                                   [-1, 9, -1],
                                   [-1, -1, -1]])

        sharpened_image = cv2.filter2D(image, -1, sharpen_filter)
        return sharpened_image

    @staticmethod
    def add_gaussian_noise(image: np.ndarray, mean=0, sigma=25):
        """
        Add Gaussian noise to the image.

        Parameters:
        image (np.ndarray): Input image.
        mean (float): Mean of the Gaussian distribution.
        sigma (float): Standard deviation of the Gaussian distribution.

        Returns:
        np.ndarray: Image with added Gaussian noise.
        """
        row, col, ch = image.shape
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy_image = np.clip(image + gauss, 0, 255).astype(np.uint8)
        return noisy_image

    def load_and_preprocess(self) -> (np.ndarray, np.ndarray):
        """
        Load images from the specified path, preprocess them and align faces.

        Returns:
        Tuple of NumPy arrays: (regular_images, infrared_images)
        """
        regular_images = []
        infrared_images = []

        regular_path = os.path.join(self.path, "regular")
        infrared_path = os.path.join(self.path, "infrared")

        # Load and preprocess regular images
        for filename in sorted(os.listdir(regular_path)):
            if filename.endswith(".bmp"):
                image = cv2.imread(os.path.join(regular_path, filename))
                sharpened_image = self.sharpen_image(image)
                noisy_image = self.add_gaussian_noise(sharpened_image)
                regular_images.append(noisy_image)

        # Load and preprocess infrared images
        for filename in sorted(os.listdir(infrared_path)):
            if filename.endswith(".bmp"):
                image = cv2.imread(os.path.join(infrared_path, filename))
                sharpened_image = self.sharpen_image(image)
                noisy_image = self.add_gaussian_noise(sharpened_image)
                infrared_images.append(noisy_image)

        return np.array(regular_images), np.array(infrared_images)

    @staticmethod
    def save_images(regular_images: np.ndarray, infrared_images: np.ndarray, output_dir: str) -> None:
        """
        Save the processed images.

        Parameters:
        regular_images (np.ndarray): Array of preprocessed regular images.
        infrared_images (np.ndarray): Array of preprocessed infrared images.
        output_dir (str): Output directory to save the images.

        Returns:
        None
        """
        os.makedirs(output_dir, exist_ok=True)

        # Save regular images
        for i, image in enumerate(regular_images):
            cv2.imwrite(os.path.join(output_dir, f"regular_{i}.bmp"), image)

        # Save infrared images
        for i, image in enumerate(infrared_images):
            cv2.imwrite(os.path.join(output_dir, f"infrared_{i}.bmp"), image)
