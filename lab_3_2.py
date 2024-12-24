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
parametr_lambda = 0.72 # Интенсивность поступления заявок
parametr_betta = 0.14 # Интенсивность обслуживания заявок
num_lines = 3 # Число линий
storage_capacity = 1 # Ёмкость накопителя
num_calls = 0 # Общее число вызовов
num_cancel_calls = 0 # Число отклонённых вызовов
load_lines = 0 # Загруженные линии
load_capacity = 0 # Загруженность накопителя
effectiveness = 0.0 # Эффективность
line_activity = []

def initialize_activity():
    global line_activity
    line_activity = [[] for _ in range(num_lines)]

def calculate():
    global simulate_time, parametr_lambda, parametr_betta, num_lines, storage_capacity, effectiveness
    try:
        simulate_time = int(entry_simulate_time.get())
        parametr_lambda = float(entry_parametr_lambda.get())
        parametr_betta = float(entry_parametr_betta.get())
        num_lines = int(entry_num_lines.get())
        storage_capacity = int(entry_storage_capacity.get())

        if simulate_time <= 0 or parametr_betta <= 0 or parametr_lambda <= 0 or num_lines <= 0 or storage_capacity < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Ошибка', 'Неправильное значение')
        return

    global load_lines, load_capacity, num_calls, num_cancel_calls, line_activity
    num_calls = 0
    num_cancel_calls = 0
    load_lines = 0
    load_capacity = 0
    capacity_time = []
    initialize_activity()

    t = 0  # Текущее время
    line_tetta = [0 for _ in range(num_lines)]  # Массив окончания обслуживания заявок

    def update(frame):
        nonlocal t
        global num_calls, num_cancel_calls, load_lines, load_capacity, line_activity, effectiveness

        if t >= simulate_time:
            anim.event_source.stop()
            return

        # Генерация времени до следующей заявки (экспоненциальное распределение)
        z_i = -log(1 - np.random.random()) / parametr_lambda
        num_calls += 1

        # Освобождение занятых линий
        for i in range(num_lines):
            if line_tetta[i] != 0 and line_tetta[i] <= t:
                line_activity[i].append((line_tetta[i], t))
                load_lines -= 1
                line_tetta[i] = 0

        # Время обслуживания заявки
        tetta_i = -log(1 - np.random.random()) / parametr_betta

        # Попытка распределить задачу по линиям в строгом порядке приоритета
        for i in range(num_lines):
            if line_tetta[i] == 0:  # Если линия свободна
                line_tetta[i] = t + tetta_i
                load_lines += 1
                break
        else:  # Если все линии заняты
            if load_capacity < storage_capacity:  # Есть место в накопителе
                load_capacity += 1
                capacity_time.append(tetta_i)
            else:  # Накопитель заполнен, заявка отклоняется
                num_cancel_calls += 1

        # Обработка накопленных заявок
        for i in range(num_lines):
            if load_capacity > 0 and line_tetta[i] == 0:  # Если линия освободилась
                line_tetta[i] = t + capacity_time.pop(0)
                load_lines += 1
                load_capacity -= 1

        lbl_out_load_lines.config(text=load_lines)
        lbl_out_load_capacity.config(text=load_capacity)
        lbl_out_num_calls.config(text=num_calls)
        lbl_out_num_cancel_calls.config(text=num_cancel_calls)
        effectiveness = (num_calls - num_cancel_calls) / num_calls if num_calls > 0 else 0
        lbl_out_effectiveness.config(text=f"{effectiveness:.2f}")

        if chk_state.get():
            # Добавление новых линий на график
            for i, intervals in enumerate(line_activity):
                if intervals:
                    start, end = intervals[-1]  # Последний интервал
                    ax.plot([start, end], [i + 1, i + 1], color='blue', linewidth=2)

        t += z_i

    if chk_state.get():
        fig, ax = plt.subplots()
        ax.set_xlabel('Время')
        ax.set_ylabel('Номер линии')
        ax.set_yticks(range(1, num_lines + 1))
        ax.grid(True)
        ax.set_title("Система массового обслуживания")
        anim = FuncAnimation(fig, update, interval=100, repeat=False)
        plt.show()
    else:
        while t <= simulate_time:
            update(1)
        plt.show()

window = Tk()
window.title("Система массового обслуживания")

lbl_simulate_time = Label(window, text="Время моделирования: ")
lbl_simulate_time.grid(row=0, column=0)
entry_simulate_time = Entry(window, width=6)
entry_simulate_time.grid(row=0, column=1)
entry_simulate_time.insert(0, str(simulate_time))

lbl_parametr_lambda = Label(window, text="Интенсивность заявок (λ): ")
lbl_parametr_lambda.grid(row=1, column=0)
entry_parametr_lambda = Entry(window, width=6)
entry_parametr_lambda.grid(row=1, column=1)
entry_parametr_lambda.insert(0, str(parametr_lambda))

lbl_parametr_betta = Label(window, text="Интенсивность обслуживания (β): ")
lbl_parametr_betta.grid(row=2, column=0)
entry_parametr_betta = Entry(window, width=6)
entry_parametr_betta.grid(row=2, column=1)
entry_parametr_betta.insert(0, str(parametr_betta))

lbl_num_lines = Label(window, text="Число линий: ")
lbl_num_lines.grid(row=3, column=0)
entry_num_lines = Entry(window, width=6)
entry_num_lines.grid(row=3, column=1)
entry_num_lines.insert(0, str(num_lines))

lbl_storage_capacity = Label(window, text="Ёмкость накопителя: ")
lbl_storage_capacity.grid(row=4, column=0)
entry_storage_capacity = Entry(window, width=6)
entry_storage_capacity.grid(row=4, column=1)
entry_storage_capacity.insert(0, str(storage_capacity))

btn_calculate = Button(window, text="Рассчитать", command=calculate)
btn_calculate.grid(row=5, column=0, columnspan=2)

lbl_num_calls = Label(window, text="Число вызовов: ")
lbl_num_calls.grid(row=6, column=0)
lbl_out_num_calls = Label(window, text=num_calls, width=6)
lbl_out_num_calls.grid(row=6, column=1)

lbl_num_cancel_calls = Label(window, text="Отклонённые вызовы: ")
lbl_num_cancel_calls.grid(row=7, column=0)
lbl_out_num_cancel_calls = Label(window, text=num_cancel_calls, width=6)
lbl_out_num_cancel_calls.grid(row=7, column=1)

lbl_load_lines = Label(window, text="Загруженные линии: ")
lbl_load_lines.grid(row=8, column=0)
lbl_out_load_lines = Label(window, text=load_lines, width=6)
lbl_out_load_lines.grid(row=8, column=1)

lbl_load_capacity = Label(window, text="Загруженность накопителя: ")
lbl_load_capacity.grid(row=9, column=0)
lbl_out_load_capacity = Label(window, text=load_capacity, width=6)
lbl_out_load_capacity.grid(row=9, column=1)

lbl_effectiveness = Label(window, text="Эффективность: ")
lbl_effectiveness.grid(row=10, column=0)
lbl_out_effectiveness = Label(window, text=f"{effectiveness:.2f}", width=6)
lbl_out_effectiveness.grid(row=10, column=1)

chk_state = BooleanVar()
chk_state.set(False)
chk = Checkbutton(window, text='Выводить график', var=chk_state)
chk.grid(row=11, column=0)

window.mainloop()
