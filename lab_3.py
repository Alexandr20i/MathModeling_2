from tkinter import Tk, Label, Entry, Button, messagebox, BooleanVar
from tkinter.ttk import Checkbutton
from math import log
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import matplotlib
matplotlib.use('TkAgg')  # Использовать TkAgg бэкенд


# Параметры системы
simulate_time = 100 # Время моделирования в минутах
parametr_lambda = 0.72 # Показатель времени (степенной параметр лямбда для потока Эрланга нулевого порядка)
parametr_betta = 0.14 # Показатель для длительности (степенной параметр бэтта для времени обслуживания)
num_lines = 3 # Число линий
storage_capacity = 1 # Ёмкость накопителя
num_calls = 0 # Общее число вызовов
num_cancel_calls = 0 # Число отклонённых вызовов
load_lines = 0 # Загруженные линии
load_capacity = 0 # Загруженность накопителя
effectiveness = 0 # Эффективность
line_activity = []
interval = 0
erlang_k = 3  # Порядок Потока Эрланга

def initialize_lines(ax):
    """Инициализация линий на графике"""
    global line_objects
    line_objects = []
    for _ in range(num_lines):
        line, = ax.plot([], [], color='blue', linewidth=2)
        line_objects.append(line)

def erlang_flow(k, lambda_param):
    """Генерация промежутков потока Эрланга с порядком k"""
    return sum(-log(1 - np.random.random()) / (lambda_param * k) for _ in range(k))

def toggle_erlang_options():
    """Показывает или скрывает ввод параметра k при активации галочки"""
    if chk_state_erlang.get():
        lbl_erlang_k.grid()
        entry_erlang_k.grid()
    else:
        lbl_erlang_k.grid_remove()
        entry_erlang_k.grid_remove()



def calculate():
    global simulate_time, parametr_lambda, parametr_betta, num_lines, storage_capacity
    try:
        simulate_time = int(entry_simulate_time.get())
        parametr_lambda = float(entry_parametr_lambda.get())
        parametr_betta = float(entry_parametr_betta.get())
        num_lines = int(entry_num_lines.get())
        storage_capacity = int(entry_storage_capacity.get())
        # erlang_k = int(entry_erlang_k.get())

        if chk_state_erlang.get():
            erlang_k = int(entry_erlang_k.get())

        if (simulate_time <= 0 or parametr_betta <= 0 or parametr_lambda <= 0 or num_lines <= 0
                or storage_capacity <= 0):
            raise ValueError
    except ValueError:
        messagebox.showerror('Ошибка', 'Неправильное значение')
        return

    global load_lines, load_capacity, effectiveness, num_calls, num_cancel_calls, line_activity
    num_calls = 0
    num_cancel_calls = 0
    load_lines = 0
    load_capacity = 0
    capacity_time = []
    line_activity = [[] for _ in range(num_lines)]  # Инициализация активности линий

    t = 0  # Текущее время
    line_tetta = [0 for _ in range(num_lines)]  # Массив, хранящий значения окончания обслуживания заявки для каждой линии

    def update(frame):
        nonlocal t
        global num_calls, num_cancel_calls, load_lines, load_capacity, line_activity

        if t >= simulate_time:
            anim.event_source.stop()
            anim.event_source.remove()  # Удаляет источник событий
            return

        # Выбор потока: Эрланг или обычный
        if chk_state_erlang.get():
            z_i = erlang_flow(erlang_k, parametr_lambda)  # k=3 для Потока Эрланга
            # print("Поток Эрланга")
        else:
            z_i = -log(1 - np.random.random()) / parametr_lambda
            # print("Экспоненциальное распределение")


        num_calls += 1

        # Освобождение занятых линий
        for i in range(num_lines):
            if line_tetta[i] != 0 and line_tetta[i] < t:
                line_activity[i].append((line_tetta[i], t))
                load_lines -= 1
                line_tetta[i] = 0

        tetta_i = -log(np.random.random()) / parametr_betta  # Время обслуживания заявки

        # if chk_state_modify.get():
        #     capacity_time.sort()
        if load_capacity == 0:  # Накопитель не заполнен
            if load_lines < num_lines:
                for i in range(num_lines):
                    if line_tetta[i] == 0:
                        line_tetta[i] = t + tetta_i
                        load_lines += 1
                        break
            else:
                load_capacity += 1
                capacity_time.append(tetta_i)

        elif load_capacity < storage_capacity:  # Накопитель заполнен частично
            if load_lines < num_lines:
                for i in range(num_lines):
                    if line_tetta[i] == 0:
                        line_tetta[i] = t + capacity_time.pop(0)
                        load_lines += 1
                        load_capacity = max(0, load_capacity - 1)
                        break
            else:
                load_capacity += 1
                capacity_time.append(tetta_i)

        else:  # Накопитель полностью заполнен
            if load_lines < num_lines:
                for i in range(num_lines):
                    if line_tetta[i] == 0:
                        line_tetta[i] = t + capacity_time.pop(0)
                        load_lines += 1
                        load_capacity -= 1
                        break
            else:
                num_cancel_calls += 1

        effectiveness = (num_calls - num_cancel_calls) / num_calls

        lbl_out_load_lines.config(text=load_lines)
        lbl_out_load_capacity.config(text=load_capacity)
        lbl_out_num_calls.config(text=num_calls)
        lbl_out_num_cancel_calls.config(text=num_cancel_calls)
        lbl_out_effectiveness.config(text=effectiveness)
        window.update()

        if chk_state.get():

            # Обновление линий на графике
            for i, line in enumerate(line_objects):
                if line_activity[i]:
                    x_data = []
                    y_data = []
                    for start, end in line_activity[i]:
                        x_data.extend([start, end])
                        y_data.extend([i + 1, i + 1])
                    line.set_data(x_data, y_data)

        t += z_i

    if chk_state.get():
        fig, ax = plt.subplots()

        ax.set_xlabel('Время')
        ax.set_ylabel('Номер линии')
        ax.set_yticks(range(num_lines + 1))
        ax.grid(True)

        if chk_state_erlang.get():
            ax.set_title("Потоки Эрланга")
        else:
            ax.set_title("Экспоненциальное распределение")

        initialize_lines(ax)  # Передача ax в функцию

        anim = FuncAnimation(fig, update, interval=0, cache_frame_data=False, blit=False, repeat=False)
        plt.show()

    else:
        while t <= simulate_time:
            update(1)
        plt.show()


window = Tk()
window.title("3 Лабораторная работа")


# Входные параметры системы
lbl_simulate_tile = Label(window, text="Время моделирования: ")
lbl_simulate_tile.grid(row=0, column=0)
entry_simulate_time = Entry(window, borderwidth=1, relief="solid", width=6)
entry_simulate_time.grid(row=0, column=1)
entry_simulate_time.insert(0, str(simulate_time))


lbl_parametr_lambda = Label(window, text="Показатель времени: ")
lbl_parametr_lambda.grid(row=0, column=3)
entry_parametr_lambda = Entry(window, borderwidth=1, relief="solid", width=6)
entry_parametr_lambda.grid(row=0, column=4)
entry_parametr_lambda.insert(0, str(parametr_lambda))

lbl_space = Label(window, width=5)
lbl_space.grid(row=0, column=5)

lbl_parametr_betta = Label(window, text="Показатель для длительности: ")
lbl_parametr_betta.grid(row=0, column=5)
entry_parametr_betta = Entry(window, borderwidth=1, relief="solid", width=6)
entry_parametr_betta.grid(row=0, column=6)
entry_parametr_betta.insert(0, str(parametr_betta))

lbl_num_lines = Label(window, text="Число линий: ")
lbl_num_lines.grid(row=1, column=0)
entry_num_lines = Entry(window, borderwidth=1, relief="solid", width=6)
entry_num_lines.grid(row=1, column=1)
entry_num_lines.insert(0, str(num_lines))

lbl_storage_capacity = Label(window, text="Ёмкость накопителя: ")
lbl_storage_capacity.grid(row=1, column=3)
entry_storage_capacity = Entry(window, borderwidth=1, relief="solid", width=6)
entry_storage_capacity.grid(row=1, column=4)
entry_storage_capacity.insert(0, str(storage_capacity))

# Выходные параметры

lbl_num_calls = Label(window, text="Число вызовов: ")
lbl_num_calls.grid(row=2, column=0)
lbl_out_num_calls = Label(window, text=num_calls, borderwidth=1, relief="solid",
                          width=6, state="disabled", bg="lightgreen")
lbl_out_num_calls.grid(row=2, column=1)

lbl_num_cancel_calls = Label(window, text="Отклонённые вызовы: ")
lbl_num_cancel_calls.grid(row=3, column=0)
lbl_out_num_cancel_calls = Label(window, text=num_cancel_calls, borderwidth=1, relief="solid",
                          width=6, state="disabled", bg="lightgreen")
lbl_out_num_cancel_calls.grid(row=3, column=1)

lbl_load_lines = Label(window, text="Загруженные линии: ")
lbl_load_lines.grid(row=2, column=3)
lbl_out_load_lines = Label(window, text=load_lines, borderwidth=1, relief="solid",
                          width=6, state="disabled", bg="lightgreen")
lbl_out_load_lines.grid(row=2, column=4)

lbl_space = Label(window, width=5)
lbl_space.grid(row=2, column=8)

lbl_load_capacity = Label(window, text="Загруженность накопителя: ")
lbl_load_capacity.grid(row=3, column=3)
lbl_out_load_capacity = Label(window, text=load_capacity, borderwidth=1, relief="solid",
                          width=6, state="disabled", bg="lightgreen")
lbl_out_load_capacity.grid(row=3, column=4)

lbl_effectiveness = Label(window, text="Эффективность: ")
lbl_effectiveness.grid(row=1, column=5)
lbl_out_effectiveness = Label(window, text=effectiveness, borderwidth=1, relief="solid",
                          width=16, state="disabled", bg="lightblue")
lbl_out_effectiveness.grid(row=1, column=6)

btn = Button(window, text="Расчёт", command=calculate)
btn.grid(row=2, column=6)

# Отрисовка графика в конце расчётов, если True
chk_state = BooleanVar()
chk_state.set(False)
chk = Checkbutton(window, text='Выводить график в конце расчётов', var=chk_state)
chk.grid(row=2, column=5)

# Включение модификации Галочка для Потока Эрланга
lbl_erlang_k = Label(window, text="Порядок Эрланга (k): ")
entry_erlang_k = Entry(window, width=6)

chk_state_erlang = BooleanVar()
chk_state_erlang.set(False)
chk_erlang = Checkbutton(window, text='Потоки Эрланга', var=chk_state_erlang, command=toggle_erlang_options)
chk_erlang.grid(row=3, column=5)

lbl_erlang_k.grid(row=3, column=6)
entry_erlang_k.grid(row=3, column=7)
lbl_erlang_k.grid_remove()
entry_erlang_k.grid_remove()


window.mainloop()
