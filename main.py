import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from io import BytesIO
from PIL import Image, ImageTk

# Разрешённые имена для вычисления выражения
allowed_names = {
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'log': np.log,
    'exp': np.exp,
    'sqrt': np.sqrt,
    'abs': np.abs,
    'pi': np.pi,
    'e': np.e
}

# Локальные переменные для sympy
sympy_locals = {
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'log': sp.log,
    'exp': sp.exp,
    'sqrt': sp.sqrt,
    'abs': sp.Abs,
    'pi': sp.pi,
    'e': sp.E
}

class PlotApp:
    def __init__(self, master):
        self.master = master
        master.title("График функции и площадь")
        master.geometry("1000x700")  # увеличенное окно
        master.configure(bg="#f0f0f0")

        # Используем стиль ttk для современного вида
        style = ttk.Style(master)
        style.theme_use("clam")

        # Основной контейнер с отступами
        container = ttk.Frame(master, padding="20")
        container.pack(fill="both", expand=True)

        # Фрейм для элементов управления
        control_frame = ttk.Frame(container)
        control_frame.pack(pady=10)

        # Ввод выражения функции
        ttk.Label(control_frame, text="Функция f(x):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.expr_entry = ttk.Entry(control_frame, width=40)
        self.expr_entry.insert(0, "(4*e)**(-4*x)")
        self.expr_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        # Привязываем событие обновления отображения формулы при изменении текста
        self.expr_entry.bind("<KeyRelease>", self.update_math_label)

        # Ярлык для отображения LaTeX-формулы как изображения
        self.math_image_label = ttk.Label(control_frame)
        self.math_image_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        self.math_photo = None  # для хранения ссылки на изображение
        self.update_math_label(None)  # инициализируем ярлык

        # Кнопка построить график
        self.plot_button = ttk.Button(control_frame, text="Построить график", command=self.plot_graph)
        self.plot_button.grid(row=0, column=3, padx=5, pady=5)

        # Ввод границ для вычисления площади
        ttk.Label(control_frame, text="x1 (от 0 до 1):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.x1_entry = ttk.Entry(control_frame, width=10)
        self.x1_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="x2 (от 0 до 1):").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.x2_entry = ttk.Entry(control_frame, width=10)
        self.x2_entry.grid(row=2, column=3, padx=5, pady=5)

        # Кнопка для вычисления площади
        self.area_button = ttk.Button(control_frame, text="Посчитать площадь", command=self.calculate_area)
        self.area_button.grid(row=2, column=4, padx=5, pady=5)

        # Метка для вывода результата площади
        self.area_label = ttk.Label(container, text="Площадь: -", font=("Helvetica", 11))
        self.area_label.pack(pady=5)

        # Фрейм для области графика
        plot_frame = ttk.Frame(container)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Начальный диапазон оси X
        self.x = np.linspace(0, 1.3, 1000)  # начинаем с большего диапазона
        self.y = np.zeros_like(self.x)

        # Привязка событий колесика мыши
        self.canvas.mpl_connect('scroll_event', self.on_scroll)

        # Переменные для dragging
        self.dragging = False
        self.x_start = 0

        # Привязка событий для dragging
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

    def update_math_label(self, event):
        expr = self.expr_entry.get()
        try:
            # Преобразуем выражение через sympy для красивого представления
            expr_sym = sp.sympify(expr, locals=sympy_locals)
            expr_latex = sp.latex(expr_sym)
        except Exception:
            expr_latex = expr
        # Формируем строку для рендеринга в LaTeX
        formula = f"$f(x) = {expr_latex}$"
        # Используем matplotlib для генерации изображения формулы
        buf = BytesIO()
        # Создаем небольшую фигуру для рендеринга формулы
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, formula, fontsize=20)
        plt.axis('off')
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=200, transparent=True)
        plt.close(fig)
        buf.seek(0)
        image = Image.open(buf)
        self.math_photo = ImageTk.PhotoImage(image)
        self.math_image_label.config(image=self.math_photo)

    def plot_graph(self):
        expr = self.expr_entry.get()
        try:
            allowed_names['x'] = self.x
            y = eval(expr, {"__builtins__": {}}, allowed_names)
            y[self.x < 0] = 0  # дополнительная защита
            self.y = y

            self.ax.clear()
            self.ax.plot(self.x, y, color="#1f77b4", lw=2)
            self.ax.set_xlim(self.x[0], self.x[-1])  # изначально показываем весь диапазон
            self.ax.set_title("График функции", fontsize=14)
            self.ax.set_xlabel("x", fontsize=12)
            self.ax.set_ylabel("")  # подпись оси Y убрана
            self.ax.grid(True)
            # Для легенды также используем красивое представление
            try:
                expr_sym = sp.sympify(expr, locals=sympy_locals)
                expr_latex = sp.latex(expr_sym)
            except Exception:
                expr_latex = expr
            self.ax.legend([f"$f(x) = {expr_latex}$"], fontsize=10)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении графика:\n{e}")

    def on_scroll(self, event):
        """
        Обработчик события колесика мыши для изменения диапазона оси X.
        При прокрутке колесика будем изменять диапазон вправо.
        """
        x_min, x_max = self.ax.get_xlim()

        # Параметры для изменения масштаба
        zoom_factor = 0.1  # коэффициент изменения масштаба
        if event.button == 'up':
            # Увеличиваем диапазон вправо
            new_x_min = x_min
            new_x_max = x_max + (x_max - x_min) * zoom_factor
        elif event.button == 'down':
            # Уменьшаем диапазон вправо
            new_x_min = x_min
            new_x_max = x_max - (x_max - x_min) * zoom_factor
        else:
            return

        # Обновляем ось X
        self.ax.set_xlim(new_x_min, new_x_max)

        # Расширяем данные x и пересчитываем y для нового диапазона
        new_x = np.linspace(new_x_min, new_x_max, 1000)  # создаем новые данные для x
        allowed_names['x'] = new_x  # обновляем x в выражении
        try:
            # Вычисляем новые значения y
            y_new = eval(self.expr_entry.get(), {"__builtins__": {}}, allowed_names)
            y_new = np.maximum(y_new, 0)  # убираем возможные отрицательные значения для y
            self.y = y_new  # обновляем y для графика

            # Перерисовываем график с новыми значениями
            self.ax.clear()
            self.ax.plot(new_x, y_new, color="#1f77b4", lw=2)
            self.ax.set_xlim(new_x_min, new_x_max)  # обновляем диапазон оси X
            self.ax.set_title("График функции", fontsize=14)
            self.ax.set_xlabel("x", fontsize=12)
            self.ax.set_ylabel("")  # подпись оси Y убрана
            self.ax.grid(True)

            # Для легенды также используем красивое представление
            expr_sym = sp.sympify(self.expr_entry.get(), locals=sympy_locals)
            expr_latex = sp.latex(expr_sym)
            self.ax.legend([f"$f(x) = {expr_latex}$"], fontsize=10)

            # Перерисовываем канвас
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при пересчете функции:\n{e}")

    def on_press(self, event):
        """Запоминаем положение мыши при нажатии для перетаскивания"""
        if event.button == 1:  # Левая кнопка мыши
            self.dragging = True
            self.x_start = event.xdata

    def on_motion(self, event):
        """Обрабатываем движение мыши при нажатой кнопке"""
        if self.dragging and event.xdata is not None:  # Добавлена проверка на None
            dx = event.xdata - self.x_start
            self.ax.set_xlim(self.ax.get_xlim() - dx)
            self.canvas.draw()
            self.x_start = event.xdata

    def on_release(self, event):
        """Завершаем перетаскивание"""
        if event.button == 1:
            self.dragging = False

    def calculate_area(self):
        try:
            x1 = float(self.x1_entry.get())
            x2 = float(self.x2_entry.get())
            if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
                raise ValueError("x1 и x2 должны быть в пределах от 0 до 1")
            if x1 >= x2:
                raise ValueError("x1 должен быть меньше x2")

            mask = (self.x >= x1) & (self.x <= x2)
            x_area = self.x[mask]
            y_area = self.y[mask]
            area = np.trapz(y_area, x_area)
            self.area_label.config(text=f"Площадь: {area:.4f}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при вычислении площади:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
