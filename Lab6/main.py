import tkinter as tk
from random import uniform


class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод Монте-Карло")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Выберите задание:").grid(row=0, column=0, sticky="w")

        self.var = tk.IntVar()
        tk.Radiobutton(self.frame, text="Определение площади фигуры", variable=self.var, value=1).grid(row=1, column=0, sticky="w")
        tk.Radiobutton(self.frame, text="Вычисление определенного интеграла", variable=self.var, value=2).grid(row=2, column=0, sticky="w")

        tk.Label(self.frame, text="Введите количество испытаний (N):").grid(row=3, column=0, sticky="w")
        self.entry_n = tk.Entry(self.frame)
        self.entry_n.grid(row=3, column=1)

        self.calculate_button = tk.Button(self.frame, text="Вычислить", command=self.calculate)
        self.calculate_button.grid(row=4, columnspan=2, pady=5)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=5, columnspan=2)

        self.error_label = tk.Label(self.frame, text="")
        self.error_label.grid(row=6, columnspan=2)

        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg='white')
        self.canvas.grid(row=7, columnspan=2, pady=10)

    def monte_carlo_area(self, area, n):
        inside = 0
        self.canvas.delete("all")
        self.draw_axes()
        for _ in range(n):
            x = uniform(-2, 2)
            y = uniform(-2, 2)
            screen_x = 200 + x * 50
            screen_y = 200 - y * 50
            if area(x, y):
                self.canvas.create_oval(screen_x - 2, screen_y - 2, screen_x + 2, screen_y + 2, fill='blue', outline='blue')
                inside += 1
            else:
                self.canvas.create_oval(screen_x - 2, screen_y - 2, screen_x + 2, screen_y + 2, fill='red', outline='red')
        return (inside / n) * 16  # S = (K / N) * S0

    def monte_carlo_integral(self, func, a, b, n):
        integral_sum = 0
        for _ in range(n):
            x = uniform(a, b)
            integral_sum += func(x)
        return (integral_sum / n) * (b - a)

    def area_condition(self, x, y):
        return x ** 2 - y ** 3 < 2 and x + y < 1

    def func(self, x):
        return x ** 2

    def draw_axes(self):
        # Draw x-axis
        self.canvas.create_line(0, 200, 400, 200, fill="black")
        # Draw y-axis
        self.canvas.create_line(200, 0, 200, 400, fill="black")

        # Draw ticks on x-axis
        for i in range(-2, 3):
            x = 200 + i * 50
            self.canvas.create_line(x, 195, x, 205, fill="black")
            self.canvas.create_text(x, 215, text=str(i), fill="black")

        # Draw ticks on y-axis
        for i in range(-2, 3):
            y = 200 - i * 50
            self.canvas.create_line(195, y, 205, y, fill="black")
            self.canvas.create_text(185, y, text=str(i), fill="black")

    def calculate(self):
        try:
            n = int(self.entry_n.get())
            if self.var.get() == 1:
                result = self.monte_carlo_area(self.area_condition, n)
                relative_error = abs(result - 6.37517) / 6.37517
                self.result_label.config(text=f"Площадь фигуры: {result:.5f}")
                self.error_label.config(text=f"Относительная погрешность: {relative_error:.5f}")
            elif self.var.get() == 2:
                result = self.monte_carlo_integral(self.func, 0, 2, n)
                analytic_result = 8 / 3  # Аналитическое решение для интеграла x^2 от 0 до 2
                relative_error = abs(result - analytic_result) / analytic_result
                self.result_label.config(text=f"Результат Монте-Карло: {result:.5f}")
                self.error_label.config(text=f"Относительная погрешность: {relative_error:.5f}")
        except ValueError:
            self.result_label.config(text="Ошибка: введите целое число для N.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MonteCarloSimulator(root)
    root.mainloop()
