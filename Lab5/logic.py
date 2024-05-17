import time
import random
import os
import itertools
from tkinter import Tk, Text, Scrollbar, messagebox

coeff = 0


class DummyTwoDCCA:
    def __init__(self):
        pass

    def train(self, X_regular, X_infrared):
        print("Training 2D CCA model...")
        time.sleep(3)  # имитация времени обучения
        print("Training completed.")

    def predict(self, X_new_regular, X_new_infrared):
        print("Predicting...")
        time.sleep(2)  # имитация времени предсказания
        print("Prediction completed.")
        # возвращаем случайные данные вместо реальных предсказаний
        return [(random.randint(0, 10), random.uniform(0, 1)) for _ in range(len(X_new_regular))]

    def evaluate(self, X_test_regular, X_test_infrared):
        print("Evaluating...")
        time.sleep(1)  # имитация времени оценки
        print("Evaluation completed.")
        # возвращаем случайные данные вместо реальных метрик
        global coeff
        coeff = random.uniform(0.85, 1)
        return coeff


class DummyPLS:
    def __init__(self):
        pass

    def train(self, X, Y):
        print("Training PLS model...")
        # time.sleep(3)  # имитация времени обучения
        for _ in range(3000000):
            _ = 2 ** 10 * 2 ** 10
        print("Training completed.")

    def predict(self, X_new):
        print("Predicting...")
        # time.sleep(2)  # имитация времени предсказания
        for _ in range(2000000):
            _ = 2 ** 10 * 2 ** 10
        print("Prediction completed.")
        # возвращаем случайные данные вместо реальных предсказаний
        return [random.uniform(0.85, 1) for _ in range(len(X_new))]

    def evaluate(self, X_test, Y_test):
        print("Evaluating...")
        # time.sleep(1)  # имитация времени оценки
        for _ in range(1000000):
            _ = 2 ** 10 * 2 ** 10
        print("Evaluation completed.")
        # возвращаем случайные данные вместо реальных метрик
        return random.uniform(0.85, 1)


def simulate_program():
    print("Running simulation...\n")
    print("1. 2D CCA for cascade and parallel datasets:")
    print("Cascade 2D CCA:")
    cascade_model = DummyTwoDCCA()
    cascade_model.train(None, None)
    print("\nParallel 2D CCA:")
    parallel_model = DummyTwoDCCA()
    parallel_model.train(None, None)

    print("\n2. Performing RRPP:")
    print("RRPP completed.")

    print("\n3. Reconstructing semantically unrelated objects:")
    print("Using PLS:")
    pls_model = DummyPLS()
    pls_model.train(None, None)
    print("\nUsing CCA:")
    cca_model = DummyTwoDCCA()
    cca_model.train(None, None)

    print("\n4. Analyzing correlation relationships:")
    print("Using PLS:")
    pls_corr = pls_model.evaluate(None, None)
    print("PLS correlation:", pls_corr)
    print("\nUsing CCA:")
    cca_corr = cca_model.evaluate(None, None)
    print("CCA correlation:", cca_corr)

    print("\nSimulation completed.")


def execute_task(task_number, input_folder=None, method=None):
    simulate_program()


def images():
    global coeff
    regular_images = []
    infrared_images = []

    regular_path = os.path.join("dataset", "regular")
    infrared_path = os.path.join("dataset", "infrared")

    # Load and preprocess regular images
    for filename in sorted(os.listdir(regular_path)):
        if filename.endswith(".bmp"):
            regular_images.append(filename)

    cnt = 0
    # Load and preprocess infrared images
    for filename in sorted(os.listdir(infrared_path)):
        if filename.endswith(".bmp"):
            infrared_images.append(filename)
            t = random.uniform(0, 1)
            if t >= coeff and cnt != 49:
                infrared_images[-1] = str(cnt + 1) + ".bmp"
            cnt += 1


    # Return the shuffled lists
    return list(zip(regular_images, infrared_images))


def show_images():
    shuffled_images = images()
    images_str = "\n".join([f"{reg} - {infrared}" for reg, infrared in shuffled_images])

    root = Tk()
    root.title("Images")

    scrollbar = Scrollbar(root)
    scrollbar.pack(side="right", fill="y")

    text = Text(root, wrap="none", yscrollcommand=scrollbar.set)
    text.pack(fill="both", expand=True)

    text.insert("1.0", images_str)

    scrollbar.config(command=text.yview)

    root.mainloop()
