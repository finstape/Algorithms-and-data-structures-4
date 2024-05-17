import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from logic import execute_task, images, show_images


class Interface(ctk.CTk):
    def __init__(self):
        """
        Constructor of the Interface class

        Returns:
        None
        """
        ctk.CTk.__init__(self)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("РЕАЛИЗАЦИЯ МЕТОДА 2D ССА")
        self.geometry("400x200")

        self.input_folder = None
        self.method_combobox = None
        self.input_folder_label = None
        self.method_label = None
        self.input_folder_button = None
        self.train_button = None
        self.run_button = None

        self.create_interface()

    def create_interface(self) -> None:
        """
        Function to create the graphical user interface

        Returns:
        None
        """
        self.input_folder_label = ctk.CTkLabel(self, text="Входная папка: не выбрана")
        self.input_folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_folder_button = ctk.CTkButton(self, text="Выбрать", command=self.select_input_folder)
        self.input_folder_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.method_label = ctk.CTkLabel(self, text="Метод:")
        self.method_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.method_combobox = ctk.CTkComboBox(self, values=["2DCCA Cascade", "2DCCA Parallel", "PLS Cascade", "PLS Parallel"])
        self.method_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.train_button = ctk.CTkButton(self, text="Обучить", command=self.train_model)
        self.train_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.run_button = ctk.CTkButton(self, text="Запустить", command=self.test_model)
        self.run_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    def select_input_folder(self) -> None:
        """
        Function to select the input folder

        Returns:
        None
        """
        self.input_folder = filedialog.askdirectory()
        if self.input_folder:
            self.input_folder_label.configure(text="Входная папка: выбрана")

    def train_model(self) -> None:
        """
        Function to train the model

        Returns:
        None
        """
        if self.input_folder is None:
            messagebox.showinfo("Ошибка", "Выберите входную папку")
            return

        threading.Thread(target=self._train_model_in_thread).start()

    def _train_model_in_thread(self) -> None:
        """
        Function to run the training model in a separate thread

        Returns:
        None
        """
        execute_task(1, input_folder=self.input_folder, method=self.method_combobox.get())

    def test_model(self) -> None:
        """
        Function to test the model

        Returns:
        None
        """
        if self.input_folder is None:
            messagebox.showinfo("Ошибка", "Выберите входную папку")
            return

        threading.Thread(target=self._test_model_in_thread).start()

    def _test_model_in_thread(self) -> None:
        """
        Function to run the testing model in a separate thread

        Returns:
        None
        """
        execute_task(2, input_folder=self.input_folder, method=self.method_combobox.get())
        show_images()


if __name__ == "__main__":
    gui = Interface()
    gui.mainloop()
