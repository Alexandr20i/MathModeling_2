import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation


class PopulationModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование популяций")

        # Основные параметры
        self.num_species = 2
        self.diff_step = 1
        self.modeling_time = 1000
        self.scale = 0.08
        self.display_num1 = 0
        self.display_num2 = 1
        self.initial_population = [200, 100]
        self.growth_rate = [0.01, -0.01]
        self.interaction_matrix = [[0, -0.0001],
                                   [0.0001, 0, ]]

        # Параметры эпидемий (по умолчанию отключены)
        self.include_epidemics = True
        self.disease_max = 1

        # Управление анимацией
        self.is_paused = False
        self.animation_running = False

        # Верхняя панель с кнопками
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.top_frame, text="Новая система", command=self.new_system).pack(side=tk.LEFT)
        tk.Button(self.top_frame, text="Параметры", command=self.parameters).pack(side=tk.LEFT)
        tk.Button(self.top_frame, text="Запуск модели", command=self.run_model).pack(side=tk.LEFT)

        # Кнопки управления анимацией
        self.pause_button = tk.Button(self.top_frame, text="Пауза", command=self.pause_animation, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT)
        self.resume_button = tk.Button(self.top_frame, text="Продолжить", command=self.resume_animation,
                                       state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.top_frame, text="Остановить", command=self.stop_animation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        # Кнопка "Доп параметры", появляющаяся только при учете эпидемий
        self.epid_parame = tk.Button(self.top_frame, text="Доп параметры", command=self.epid_parameters)
        if self.include_epidemics == True: self.epid_parame.pack(side=tk.LEFT)
        else: self.epid_parame.pack(side=tk.LEFT)
        # self.epid_parame.pack_forget()  # Скрыта по умолчанию


        # Поле для графика
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Панель для показателей популяций и времени
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.time_label = tk.Label(self.info_frame, text="Время: 0", font=("Arial", 14))
        self.time_label.pack(pady=10)

        self.population_labels = []
        for i in range(self.num_species):
            label = tk.Label(self.info_frame, text=f"Популяция {i + 1}: {self.initial_population[i]}",
                             font=("Arial", 14))
            label.pack(pady=5)
            self.population_labels.append(label)

    def new_system(self):
        # Окно для создания новой системы
        new_system_window = tk.Toplevel(self.root)
        new_system_window.title("Новая система")

        tk.Label(new_system_window, text="Введите количество видов:").grid(row=0, column=0)
        num_species_entry = tk.Entry(new_system_window)
        num_species_entry.insert(0, str(self.num_species))
        num_species_entry.grid(row=0, column=1)

        include_epidemics_var = tk.BooleanVar(value=self.include_epidemics)
        tk.Checkbutton(new_system_window, text="Учитывать заболевания и эпидемии?",
                       variable=include_epidemics_var).grid(row=1, columnspan=2)

        def save_new_system():
            try:
                self.num_species = int(num_species_entry.get())
                self.include_epidemics = include_epidemics_var.get()
                self.initial_population = [100] * self.num_species
                self.growth_rate = [0.01] * self.num_species
                self.interaction_matrix = [[0] * self.num_species for _ in range(self.num_species)]
                if self.include_epidemics:
                    self.beta = [0.001] * self.num_species
                    self.gamma = [0.1] * self.num_species
                    self.initial_infected = [10] * self.num_species
                    self.epid_parame.pack(side=tk.LEFT)  # Показываем кнопку "Доп параметры"
                else:
                    self.beta = []
                    self.gamma = []
                    self.initial_infected = []
                    self.epid_parame.pack_forget()  # Скрываем кнопку "Доп параметры"
                self.update_population_labels()
                new_system_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Количество видов должно быть целым числом.")

        tk.Button(new_system_window, text="Сохранить", command=save_new_system).grid(row=2, columnspan=2)

    def update_population_labels(self):
        for label in self.population_labels:
            label.destroy()
        self.population_labels = []
        for i in range(self.num_species):
            label = tk.Label(self.info_frame, text=f"Популяция {i + 1}: {self.initial_population[i]}",
                             font=("Arial", 14))
            label.pack(pady=5)
            self.population_labels.append(label)

    def parameters(self):
        # Окно для настройки параметров
        param_window = tk.Toplevel(self.root)
        param_window.title("Параметры")

        # Общие параметры
        tk.Label(param_window, text="Шаг дифференцирования").grid(row=0, column=0)
        diff_step_entry = tk.Entry(param_window)
        diff_step_entry.insert(0, str(self.diff_step))
        diff_step_entry.grid(row=0, column=1)

        tk.Label(param_window, text="Время моделирования").grid(row=1, column=0)
        modeling_time_entry = tk.Entry(param_window)
        modeling_time_entry.insert(0, str(self.modeling_time))
        modeling_time_entry.grid(row=1, column=1)

        tk.Label(param_window, text="Масштаб отображения").grid(row=2, column=0)
        scale_entry = tk.Entry(param_window)
        scale_entry.insert(0, str(self.scale))
        scale_entry.grid(row=2, column=1)

        tk.Label(param_window, text="Номера отображения").grid(row=3, column=0)
        display_num1_entry = tk.Entry(param_window, width=5)
        display_num1_entry.insert(0, str(self.display_num1))
        display_num1_entry.grid(row=3, column=1, sticky='w')
        display_num2_entry = tk.Entry(param_window, width=5)
        display_num2_entry.insert(0, str(self.display_num2))
        display_num2_entry.grid(row=3, column=1, sticky='e')

        # Параметры видов
        tk.Label(param_window, text="Численность и прирост популяций").grid(row=4, column=0, columnspan=2, pady=(10, 0))
        pop_entries = []
        growth_entries = []
        for i in range(self.num_species):
            tk.Label(param_window, text=f"Популяция {i + 1}").grid(row=5 + i, column=0)
            init_pop_entry = tk.Entry(param_window)
            init_pop_entry.insert(0, str(self.initial_population[i]))
            init_pop_entry.grid(row=5 + i, column=1)
            pop_entries.append(init_pop_entry)

            growth_rate_entry = tk.Entry(param_window)
            growth_rate_entry.insert(0, str(self.growth_rate[i]))
            growth_rate_entry.grid(row=5 + i, column=2)
            growth_entries.append(growth_rate_entry)

        # Коэффициенты взаимодействия популяций
        tk.Label(param_window, text="Коэффициенты взаимодействия популяций").grid(row=5 + self.num_species, column=0,
                                                                                  columnspan=3, pady=(10, 0))
        interaction_entries = []
        for i in range(self.num_species):
            row_entries = []
            for j in range(self.num_species):
                interaction_entry = tk.Entry(param_window, width=10)
                interaction_entry.insert(0, str(self.interaction_matrix[i][j]))
                interaction_entry.grid(row=6 + self.num_species + i, column=j)
                row_entries.append(interaction_entry)
            interaction_entries.append(row_entries)

        # Кнопка для сохранения параметров
        def save_species_params():
            # Сохранение общих параметров
            self.diff_step = float(diff_step_entry.get())
            self.modeling_time = int(modeling_time_entry.get())
            self.scale = float(scale_entry.get())
            self.display_num1 = int(display_num1_entry.get())
            self.display_num2 = int(display_num2_entry.get())

            # Сохранение параметров популяций
            for i in range(self.num_species):
                self.initial_population[i] = float(pop_entries[i].get())
                self.growth_rate[i] = float(growth_entries[i].get())
                for j in range(self.num_species):
                    self.interaction_matrix[i][j] = float(interaction_entries[i][j].get())

            # Обновление меток популяций
            self.update_population_labels()

            param_window.destroy()

        tk.Button(param_window, text="Сохранить параметры", command=save_species_params).grid(row=10 + self.num_species,
                                                                                              columnspan=3)

    def pause_animation(self):
        if self.ani and not self.is_paused:
            self.ani.event_source.stop()
            self.is_paused = True
            self.resume_button.config(state=tk.NORMAL)

    def resume_animation(self):
        if self.ani and self.is_paused:
            self.ani.event_source.start()
            self.is_paused = False

    def stop_animation(self):
        if self.ani:  # Проверяем, существует ли объект анимации
            # self.ani.event_source.stop()  # Останавливаем текущую анимацию
            self.ani = None  # Сбрасываем объект анимации
        self.is_paused = False
        self.animation_running = False
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.ax.clear()  # Очищаем график
        self.canvas.draw()  # Обновляем отображение

    def epid_parameters(self):
        # Окно для настройки параметров эпидемии
        epid_param_window = tk.Toplevel(self.root)
        epid_param_window.title("Параметры эпидемии")

        # Максимальное значение болезни
        tk.Label(epid_param_window, text="Максимальное значение болезни (A_max):").grid(row=0, column=0)
        disease_max_entry = tk.Entry(epid_param_window)
        disease_max_entry.insert(0, str(self.disease_max))
        disease_max_entry.grid(row=0, column=1)

        # Период эпидемии
        tk.Label(epid_param_window, text="Период эпидемии (T):").grid(row=1, column=0)
        epidemic_period_entry = tk.Entry(epid_param_window)
        epidemic_period_entry.insert(0, str(self.modeling_time))
        epidemic_period_entry.grid(row=1, column=1)

        # Чекбокс для включения эпидемии
        include_epidemics_var = tk.BooleanVar(value=self.include_epidemics)
        tk.Checkbutton(epid_param_window, text="Учитывать эпидемию", variable=include_epidemics_var).grid(row=2,
                                                                                                          columnspan=2)

        def save_epid_parameters():
            try:
                self.disease_max = float(disease_max_entry.get())
                self.modeling_time = float(epidemic_period_entry.get())
                self.include_epidemics = include_epidemics_var.get()
                # messagebox.showinfo("Успешно", "Параметры эпидемии сохранены.")
                epid_param_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные значения.")

        tk.Button(epid_param_window, text="Сохранить", command=save_epid_parameters).grid(row=3, columnspan=2)
    def run_model(self):
        if self.animation_running:
            return


        self.animation_running = True
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

        if self.include_epidemics:
            self.run_epidemic_model()
        else:
            self.run_basic_model()

    def run_basic_model(self):
        # Базовая модель
        def population_dynamics(N, t, growth_rate, interaction_matrix):
            dN_dt = []
            for i in range(len(N)):
                rate = growth_rate[i] * N[i]
                interaction_effect = sum(interaction_matrix[i][j] * N[i] * N[j] for j in range(len(N)))
                dN_dt.append(rate + interaction_effect)
            return dN_dt

        t = np.linspace(0, self.modeling_time, int(self.modeling_time / self.diff_step))
        result = odeint(population_dynamics, self.initial_population, t,
                        args=(self.growth_rate, self.interaction_matrix))

        # Анимация
        def animate(i):
            self.ax.clear()
            for j in range(self.num_species):
                self.ax.plot(t[:i], result[:i, j], label=f"Популяция {j + 1}")
            self.ax.set_xlabel("Время")
            self.ax.set_ylabel("Численность")
            self.ax.legend()
            self.ax.grid(True)
            self.time_label.config(text=f"Время: {t[i]:.2f}")
            for k in range(self.num_species):
                self.population_labels[k].config(text=f"Популяция {k + 1}: {int(result[i, k])}")

        self.ani = FuncAnimation(self.figure, animate, frames=len(t), interval=100, repeat=False)

        self.canvas.draw()

    def run_epidemic_model(self):
        def epidemic_dynamics(N, t, growth_rate, interaction_matrix, disease_max):
            dN_dt = []
            for i in range(len(N)):
                # Рассчитываем плавное воздействие эпидемии
                Ai = disease_max * np.sin(2 * np.pi * t / self.modeling_time)
                Ai = max(0, Ai)  # Учитываем только положительное воздействие эпидемии

                # Основное уравнение
                rate = growth_rate[i] * N[i]
                interaction_effect = sum(interaction_matrix[i][j] * N[i] * N[j] for j in range(len(N)))
                change = rate + interaction_effect - Ai

                # Устанавливаем ограничение: численность не может быть меньше нуля
                new_population = max(0, N[i] + change * self.diff_step)
                dN_dt.append(new_population - N[i])  # Производная
            return dN_dt

        t = np.linspace(0, self.modeling_time, int(self.modeling_time / self.diff_step))
        result = odeint(epidemic_dynamics, self.initial_population, t,
                        args=(self.growth_rate, self.interaction_matrix, self.disease_max))

        self.animate_results(result, t)

    def animate_results(self, result, t):
        def animate(i):
            self.ax.clear()
            for j in range(self.num_species):
                self.ax.plot(t[:i], result[:i, j], label=f"Популяция {j + 1}")
            self.ax.set_xlabel("Время")
            self.ax.set_ylabel("Численность")
            self.ax.legend()
            self.ax.grid(True)
            self.time_label.config(text=f"Время: {t[i]:.2f}")
            for k in range(self.num_species):
                self.population_labels[k].config(text=f"Популяция {k + 1}: {int(result[i, k])}")

        self.ani = FuncAnimation(self.figure, animate, frames=len(t), interval=100, repeat=False)
        self.canvas.draw()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PopulationModelApp(root)
    root.mainloop()
