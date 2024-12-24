import math
from tkinter import *
import tkinter.messagebox

import numpy as np

import back
import matplotlib.pyplot as plt


class Window:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"+100+75")
        self.root.resizable(False, False)
        self.efficiency = StringVar(value="0")
        self.impr = True
        self.t = StringVar(value=str(back.T))
        self.alpha = StringVar(value=str(back.alpha))
        self.beta = StringVar(value=str(back.betta))
        self.n = StringVar(value=str(back.N))
        self.c = StringVar(value=str(back.c))
        self.lineCost = StringVar(value=str('0'))
        self.capacityCost = StringVar(value=str('0'))
        self.sumCost = StringVar(value='0')
        # self.erlang = StringVar(value=str(back.error))

        self.disp_count = StringVar(value='0')
        self.rejected = StringVar(value='0')
        self.busy = StringVar(value='0')
        self.workload = StringVar(value='0')

        self.fig = self.ax = self.canvas = None

    def run(self):
        self.draw()
        self.root.mainloop()

    def draw(self):
        big_frame = LabelFrame(self.root, borderwidth=0, highlightthickness=0)
        big_frame.pack(padx=5, pady=5, ipadx=5, ipady=5)

        frame = Frame(big_frame)
        frame.pack()
        Label(frame, text="Р’СЂРµРјСЏ РјРѕРґРµР»РёСЂРѕРІР°РЅРёСЏ:").pack(side=LEFT)
        Entry(frame, width=8, textvariable=self.t).pack(side=LEFT)
        Label(frame, text="РџРѕРєР°Р·Р°С‚РµР»СЊ РґР»СЏ РІСЂРµРјРµРЅРё:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.alpha).pack(side=LEFT)
        Label(frame, text="РџРѕРєР°Р·Р°С‚РµР»СЊ РґР»СЏ РґР»РёС‚РµР»СЊРЅРѕСЃС‚Рё:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.beta).pack(side=LEFT)
        frame = Frame(big_frame)
        frame.pack(pady=(6, 0))
        Label(frame, text="Р§РёСЃР»Рѕ Р»РёРЅРёР№:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.n).pack(side=LEFT)
        Label(frame, text="Р•РјРєРѕСЃС‚СЊ РЅР°РєРѕРїРёС‚РµР»СЏ:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.c).pack(side=LEFT)
        Label(frame, text="РЎС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ Р»РёРЅРёРё:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.lineCost).pack(side=LEFT)
        Label(frame, text="РЎС‚РѕРёРјРѕСЃС‚СЊ РѕР±СЃР»СѓР¶РёРІР°РЅРёСЏ СЏС‡РµР№РєРё:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.capacityCost).pack(side=LEFT)
        # Label(frame, text="РџР°СЂР°РјРµС‚СЂ Р­СЂР»Р°РЅРіР°:").pack(side=LEFT, padx=(10, 0))
        # Entry(frame, width=8, textvariable=self.erlang).pack(side=LEFT)

        big_frame.pack(padx=5, pady=5, ipadx=5, ipady=5)
        Label(frame, text="РС‚РѕРіРѕРІР°СЏ СЃС‚РѕРёРјРѕСЃС‚СЊ:").pack(side=LEFT, padx=(10, 0))
        Entry(frame, width=8, textvariable=self.sumCost).pack(side=LEFT)
        Label(big_frame, text="Р§РёСЃР»Рѕ РІС‹Р·РѕРІРѕРІ:").pack(side=LEFT)
        Entry(big_frame, width=8, textvariable=self.disp_count).pack(
            side=LEFT)
        Label(big_frame, text="Р—Р°РіСЂСѓР¶РµРЅРЅС‹Рµ Р»РёРЅРёРё:").pack(side=LEFT, padx=(10, 0))
        Entry(big_frame, width=8, textvariable=self.busy).pack(
            side=LEFT)
        Label(big_frame, text="РћС‚РєР»РѕРЅРµРЅРЅС‹Рµ РІС‹Р·РѕРІС‹:").pack(side=LEFT, padx=(10, 0))
        Entry(big_frame, width=8, textvariable=self.rejected).pack(
            side=LEFT)
        Label(big_frame, text="РњРѕРґРµР»СЊРЅРѕРµ СѓР»СѓС‡С€РµРЅРёРµ: ").pack(side=LEFT, padx=(10, 0))
        self.toggle_button = Button(big_frame, text="Р’РљР›", width=10, command=self.Simpletoggle)
        self.toggle_button.pack(side=LEFT)
        big_frame = Frame(self.root)
        big_frame.pack(pady=5)
        Label(big_frame, text="Р­С„С„РµРєС‚РёРІРЅРѕСЃС‚СЊ:").pack(side=LEFT)
        Entry(big_frame, width=20, textvariable=self.efficiency).pack(
            side=LEFT)
        Button(big_frame, width=10, text="start", command=self.start_exec).pack(side=LEFT, padx=15)

    def set_values(self):
        t = self.t.get()
        a = self.alpha.get()
        b = self.beta.get()
        n = self.n.get()
        c = self.c.get()
        lineCost = self.lineCost.get()
        capacityCost = self.capacityCost.get()
        sumCost  = lineCost + capacityCost
        # erl = self.erlang.get()
        erl = 1
        if t.isdigit() and n.isdigit() and c.isdigit() and erl.isdigit() and back.is_float(a) and back.is_float(b):
            t = int(t)
            n = int(n)
            c = int(c)
            erl = int(erl)
            if t < 1 or n < 1 or c < 1 or erl < 1:
                tkinter.messagebox.showerror("РћС€РёР±РєР°", "Р—РЅР°С‡РµРЅРёРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ Р±РѕР»СЊС€Рµ 0")
                return False
            a = float(a)
            b = float(b)

            if a < 0 or b < 0:
                tkinter.messagebox.showerror("РћС€РёР±РєР°", "Р—РЅР°С‡РµРЅРёРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ Р±РѕР»СЊС€Рµ 0")
                return False
        else:
            tkinter.messagebox.showerror("РћС€РёР±РєР°", "Р’РІРµРґРµРЅРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ РЅРµ СЏРІР»СЏРµС‚СЃСЏ С‡РёСЃР»РѕРј")
            return False
        return True
    def Simpletoggle(self):
        if self.toggle_button.config('text')[-1] == 'Р’РљР›':
            self.toggle_button.config(text='Р’Р«РљР›')
            self.impr = False
        else:
            self.toggle_button.config(text='Р’РљР›')
            self.impr = True

    def start_exec(self):
        plt.close()
        T = int(self.t.get())
        N = int(self.n.get())
        alpha = float(self.alpha.get())
        betta = float(self.beta.get())
        c = int(self.c.get())
        error = 0
        LineCost = float(self.lineCost.get())
        CapacityCost = float(self.capacityCost.get())
        t_array = back.splitting_time(T, alpha, N,self.impr)
        d_array = back.calls_duration(len(t_array), betta)
        # if int(self.erlang.get()) != 0:
        #     t_array = [a for index, a in enumerate(t_array) if index % int(self.erlang.get()) == 0]
        #     d_array = [a for index, a in enumerate(d_array) if index % int(self.erlang.get()) == 0]
        print(f"Р”Р»РёРЅР° РјР°СЃСЃРёРІР° РЅР°С‡Р°Р»Р° Р·РІРѕРЅРєРѕРІ:{len(t_array)}   Р”Р»РёРЅР° РјР°СЃСЃРёРІР° РґР»РёС‚РµР»СЊРЅРѕСЃС‚Рё Р·РІРѕРЅРєРѕРІ:{len(d_array)}")
        print("РњР°СЃСЃРёРІ РЅР°С‡Р°Р»Р° Р·РІРѕРЅРєРѕРІ:", t_array, '\nРњР°СЃСЃРёРІ РґР»РёС‚РµР»СЊРЅРѕСЃС‚Рё Р·РІРѕРЅРєРѕРІ:', d_array)
        matrix = np.zeros((N, math.ceil(T / 0.1)), dtype=float)
        points_matrix = np.zeros((N, math.ceil(T / 0.1)), dtype=float)
        print(np.shape(matrix))
        number = 0
        k = 0
        for i in range(len(t_array)):
            start_index = int(t_array[i] / 0.1)
            end_of_call = t_array[i] + d_array[i]
            end_index = int(end_of_call / 0.1)
            if end_of_call > T:
                end_index = math.ceil(T / 0.1) - 1
            if i == 0:
                for j in range(start_index, end_index + 1):
                    matrix[0][j] += 1
                    number = 0
            else:
                id = []
                for j in range(start_index, end_index + 1):
                    id.append(j)
                flag = False
                for line in range(0, N):
                    if np.any(matrix[line][id] != 0):
                        continue
                    else:
                        matrix[line][id] += 1
                        number = line
                        flag = True
                        break
                if not flag:
                    for line in range(0, N):
                        if np.all(matrix[line][id] < c):
                            matrix[line][id] += 1
                            number = line
                            flag = True
                            break

                if not flag:
                    error += 1
                    number = float('nan')
            if number >= 0:
                k += 1
                for j in range(start_index, end_index + 1):
                    t = 0
                    for i in range(matrix.shape[0]):
                        if matrix[i][j] != 0:
                            t += 1
                print(
                    f" {k} Р—РІРѕРЅРѕРє РІР·СЏР» РєР°РЅР°Р» в„– {number + 1} РќР°С‡Р°Р»Рѕ Р·РІРѕРЅРєР°: {start_index} РљРѕРЅРµС†: {end_index} РџСЂРѕРґРѕР»Р¶РёС‚РµР»СЊРЅРѕСЃС‚СЊ: {end_of_call} Р­С„С„РµРєС‚РёРІРЅРѕСЃС‚СЊ: {k / (k + error)}")
                points_matrix[number][start_index] = number + 1
                ef = k / (k + error)
                self.efficiency.set(str(ef))
                self.disp_count.set(str(k))
                self.rejected.set((str(error)))
                self.sumCost.set(N * LineCost + c * CapacityCost)
                points_matrix[number][end_index] = number + 1
        print(f"РћС‚РєР»РѕРЅРµРЅС‹Рµ РІС‹Р·РѕРІС‹: {error}")
        busy_lines = back.get_busy_line(matrix)
        self.busy.set(str(busy_lines))
        print(f"Р—Р°РіСЂСѓР¶РµРЅРЅС‹Рµ Р»РёРЅРёРё: {busy_lines}")
        plot_array = np.linspace(0, T, math.ceil(T / 0.1))
        for i in range(np.shape(matrix)[0]):
            for j in range(np.shape(matrix)[1]):
                if matrix[i][j] == 0:
                    matrix[i][j] = float('nan')
                else:
                    matrix[i][j] = (i + 1)
                if points_matrix[i][j] == 0:
                    points_matrix[i][j] = float('nan')
        print('d')
        for i in range(np.shape(matrix)[0]):
            plt.plot(plot_array, matrix[i][:], c='red')
            plt.scatter(plot_array, points_matrix[i][:], 10,
                        c='red')

        plt.xlabel("Р’СЂРµРјСЏ")
        plt.grid()
        plt.ylabel("РљР°РЅР°Р»С‹")
        plt.locator_params(axis='x', nbins=20)
        plt.locator_params(axis='y', nbins=N)

        plt.show()

window = Window("Р›Р  в„–3")
window.run()