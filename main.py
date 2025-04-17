import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from PIL import Image, ImageTk

class ExponentialDistributionApp:
    def __init__(self, master):
        self.master = master
        master.title("Показательное распределение")
        master.geometry("1000x700")
        master.configure(bg="#f0f0f0")

        style = ttk.Style(master)
        style.theme_use("clam")

        container = ttk.Frame(master, padding="20")
        container.pack(fill="both", expand=True)

        control_frame = ttk.Frame(container)
        control_frame.pack(pady=10)

        # Ввод параметра λ
        ttk.Label(control_frame, text="Параметр λ (>0):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.lambda_entry = ttk.Entry(control_frame, width=15)
        self.lambda_entry.insert(0, "1")
        self.lambda_entry.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка построения графика
        self.plot_button = ttk.Button(control_frame, text="Построить график", command=self.plot_graph)
        self.plot_button.grid(row=0, column=2, padx=5, pady=5)

        # Отображение формулы
        self.math_image_label = ttk.Label(control_frame)
        self.math_image_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.math_photo = None
        self.update_math_label()

        # Поля для ввода границ
        ttk.Label(control_frame, text="x1 ≥ 0:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.x1_entry = ttk.Entry(control_frame, width=10)
        self.x1_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="x2 ≥ 0:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.x2_entry = ttk.Entry(control_frame, width=10)
        self.x2_entry.grid(row=2, column=3, padx=5, pady=5)

        # Кнопка для вычисления вероятности
        self.prob_button = ttk.Button(control_frame, text="Вычислить вероятность", command=self.calculate_probability)
        self.prob_button.grid(row=2, column=4, padx=5, pady=5)

        # Метка для вывода результата
        self.result_label = ttk.Label(container, text="Вероятность: -", font=("Helvetica", 11))
        self.result_label.pack(pady=5)

        # Область графика
        plot_frame = ttk.Frame(container)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.line = None
        self.x = np.array([])
        self.y = np.array([])
        self.current_lambda = 1.0
        self.fixed_y_lim = None

        # Привязка событий
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.lambda_entry.bind("<KeyRelease>", self.on_lambda_change)

        self.dragging = False
        self.x_start = 0

    def format_number(self, num):
        """Форматирует число, убирая .0 для целых значений"""
        if isinstance(num, (int, float)):
            if num.is_integer():
                return str(int(num))
            return f"{num:.2f}".rstrip('0').rstrip('.') if '.' in f"{num:.2f}" else f"{num:.2f}"
        return str(num)

    def update_math_label(self, event=None):
        try:
            lambda_val = float(self.lambda_entry.get())
            if lambda_val <= 0:
                formula = "Недопустимое значение λ (должно быть >0)"
            else:
                formatted_lambda = self.format_number(lambda_val)
                formula = f"$f(x) = {formatted_lambda}e^{{-{formatted_lambda}x}}$"
        except:
            formula = "$f(x) = \lambda e^{-\lambda x}$"
        
        # Для текстового сообщения используем обычный Label
        if "Недопустимое" in formula:
            self.math_image_label.config(text=formula, font=("Helvetica", 10, "bold"), foreground="red")
            if self.math_photo:
                self.math_image_label.config(image=None)
                self.math_photo = None
        else:
            # Для формулы используем изображение LaTeX
            buf = BytesIO()
            fig = plt.figure(figsize=(0.01, 0.01))
            fig.text(0, 0, formula, fontsize=20)
            plt.axis('off')
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=200, transparent=True)
            plt.close(fig)
            buf.seek(0)
            image = Image.open(buf)
            self.math_photo = ImageTk.PhotoImage(image)
            self.math_image_label.config(image=self.math_photo, text="")

    def on_lambda_change(self, event):
        self.update_math_label()
        if self.line:
            self.plot_graph()

    def plot_graph(self):
        try:
            lambda_val = float(self.lambda_entry.get())
            
            # Проверка на допустимость значения λ
            if lambda_val <= 0:
                messagebox.showerror("Ошибка", 
                    "Недопустимое значение параметра λ!\n\n"
                    "В показательном распределении параметр λ должен быть строго больше нуля.\n"
                    "Пожалуйста, введите положительное число.")
                return
            
            self.current_lambda = lambda_val
            
            x_min, x_max = 0, 10/lambda_val  # Начальный диапазон
            self.x = np.linspace(x_min, x_max, 1000)
            self.y = lambda_val * np.exp(-lambda_val * self.x)

            if self.line is None:
                self.line, = self.ax.plot(self.x, self.y, color="#1f77b4", lw=2)
                self.ax.set_xlim(x_min, x_max)
                self.fixed_y_lim = self.ax.get_ylim()
            else:
                self.line.set_data(self.x, self.y)
            
            self.ax.set_ylim(self.fixed_y_lim)
            
            formatted_lambda = self.format_number(lambda_val)
            self.ax.set_title(f"Плотность вероятности (λ={formatted_lambda})", fontsize=14)
            self.ax.set_xlabel("x", fontsize=12)
            self.ax.grid(True)
            self.canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Пожалуйста, введите корректное число для λ.\n\nОшибка: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении графика:\n{e}")

    def update_plot_data(self):
        if self.line is None:
            return

        x_min, x_max = self.ax.get_xlim()
        self.x = np.linspace(max(x_min, 0), x_max, 1000)
        self.y = self.current_lambda * np.exp(-self.current_lambda * self.x)
        
        self.line.set_data(self.x, self.y)
        self.ax.set_ylim(self.fixed_y_lim)
        self.canvas.draw()

    def on_scroll(self, event):
        x_min, x_max = self.ax.get_xlim()
        zoom_factor = 0.1
        
        if event.button == 'up':
            new_x_max = x_max + (x_max - x_min) * zoom_factor
            self.ax.set_xlim(x_min, new_x_max)
        elif event.button == 'down':
            new_x_max = max(x_min + 0.1, x_max - (x_max - x_min) * zoom_factor)
            self.ax.set_xlim(x_min, new_x_max)
        
        self.update_plot_data()

    def on_press(self, event):
        if event.button == 1:
            self.dragging = True
            self.x_start = event.xdata

    def on_motion(self, event):
        if self.dragging and event.xdata is not None:
            dx = event.xdata - self.x_start
            current_xlim = self.ax.get_xlim()
            new_xlim = (max(current_xlim[0] - dx, 0), current_xlim[1] - dx)
            self.ax.set_xlim(new_xlim)
            self.x_start = event.xdata
            self.update_plot_data()

    def on_release(self, event):
        if event.button == 1:
            self.dragging = False

    def calculate_probability(self):
        try:
            # Сначала проверяем λ
            lambda_val = float(self.lambda_entry.get())
            if lambda_val <= 0:
                messagebox.showerror("Ошибка", 
                    "Невозможно вычислить вероятность!\n\n"
                    "Параметр λ должен быть больше нуля для показательного распределения.")
                return
                
            x1 = float(self.x1_entry.get())
            x2 = float(self.x2_entry.get())
            
            if x1 < 0 or x2 < 0:
                raise ValueError("x должен быть ≥ 0")
            if x1 >= x2:
                raise ValueError("x1 должен быть меньше x2")
            
            mask = (self.x >= x1) & (self.x <= x2)
            prob = np.trapz(self.y[mask], self.x[mask])
            
            self.ax.fill_between(self.x[mask], self.y[mask], color="orange", alpha=0.3)
            self.ax.set_ylim(self.fixed_y_lim)
            self.canvas.draw()
            
            self.result_label.config(text=f"P({self.format_number(x1)} ≤ X ≤ {self.format_number(x2)}) = {prob:.4f}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при вычислении вероятности:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExponentialDistributionApp(root)
    root.mainloop()