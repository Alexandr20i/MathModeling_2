import math
import random

import numpy as np
import matplotlib.pyplot as plt

T = 100
N = 3
alpha = 0.1
betta = 0.1
c = 1
t = 0.0
error = 0

matrix = []
points_matrix = []
plot_array = []


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def splitting_time(Time: float, alpha: float, N: int, impr: bool = True):
    if impr:
        print("РЎ СѓР»СѓС‡С€РµРЅРёРµРј")
    else:
        print("Р‘РµР· СѓР»СѓС‡С€РµРЅРёСЏ")
    t = 0.0
    time_array = []
    while True:
        if impr:
            t += random.expovariate(alpha) * random.normalvariate(alpha) / 3
        else:
            t += random.expovariate(alpha) / 3

        if t > Time:
            return time_array
        time_array.append(t)


def calls_duration(I: int, betta: float):
    dur_array = []
    for i in range(I):
        dur_array.append(random.expovariate(betta))
    return dur_array


def get_busy_line(matrix: np.ndarray):
    free_lines = 0
    for i in range(matrix.shape[0]):
        if np.all(matrix[i][:] == 0):
            free_lines += 1
    return matrix.shape[0] - free_lines

# def func_start():
#     print("Start 11:12")
#     t = 0.0
#     global error
#     global N
#     global alpha
#     global betta
#     global c

#     t_array = splitting_time(T, alpha, N)
#     d_array = calls_duration(len(t_array), betta)
#     print(f"Р”Р»РёРЅР° РјР°СЃСЃРёРІР° РЅР°С‡Р°Р»Р° Р·РІРѕРЅРєРѕРІ:{len(t_array)}   Р”Р»РёРЅР° РјР°СЃСЃРёРІР° РґР»РёС‚РµР»СЊРЅРѕСЃС‚Рё Р·РІРѕРЅРєРѕРІ:{len(d_array)}")
#     print("РњР°СЃСЃРёРІ РЅР°С‡Р°Р»Р° Р·РІРѕРЅРєРѕРІ:", t_array, '\nРњР°СЃСЃРёРІ РґР»РёС‚РµР»СЊРЅРѕСЃС‚Рё Р·РІРѕРЅРєРѕРІ:', d_array)
#     matrix = np.zeros((N, math.ceil(T / 0.1)), dtype=float)
#     points_matrix = np.zeros((N, math.ceil(T / 0.1)), dtype=float)
#     print(np.shape(matrix))
#     number = 0
#     k = 0
#     for i in range(len(t_array)):
#         start_index = int(t_array[i] / 0.1)
#         end_of_call = t_array[i] + d_array[i]
#         end_index = int(end_of_call / 0.1)
#         if end_of_call > T:
#             end_index = math.ceil(T / 0.1) - 1
#         if i == 0:
#             for j in range(start_index, end_index + 1):
#                 matrix[0][j] += 1
#                 number = 0
#         else:
#             id = []
#             for j in range(start_index, end_index + 1):
#                 id.append(j)
#             flag = False
#             for line in range(0, N):
#                 if np.any(matrix[line][id] != 0):
#                     continue
#                 else:
#                     matrix[line][id] += 1
#                     number = line
#                     flag = True
#                     break
#             if not flag:
#                 for line in range(0, N):
#                     if np.all(matrix[line][id] < c):
#                         matrix[line][id] += 1
#                         number = line
#                         flag = True
#                         break

#             if not flag:
#                 error += 1
#                 number = float('nan')
#         if number >= 0:
#             k += 1
#             for j in range(start_index, end_index + 1):
#                 t = 0
#                 for i in range(matrix.shape[0]):
#                     if matrix[i][j] != 0:
#                         t += 1
#             print(
#                 f" {k} Р—РІРѕРЅРѕРє РІР·СЏР» РєР°РЅР°Р» в„– {number + 1} РќР°С‡Р°Р»Рѕ Р·РІРѕРЅРєР°: {start_index} РљРѕРЅРµС†: {end_index} РџСЂРѕРґРѕР»Р¶РёС‚РµР»СЊРЅРѕСЃС‚СЊ: {end_of_call} Р­С„С„РµРєС‚РёРІРЅРѕСЃС‚СЊ: {k / (k + error)}")
#             points_matrix[number][start_index] = number + 1
#             points_matrix[number][end_index] = number + 1
#     print(f"РћС‚РєР»РѕРЅРµРЅС‹Рµ РІС‹Р·РѕРІС‹: {error}")
#     busy_lines = get_busy_line(matrix)
#     print(f"Р—Р°РіСЂСѓР¶РµРЅРЅС‹Рµ Р»РёРЅРёРё: {busy_lines}")
#     plot_array = np.linspace(0, T, math.ceil(T / 0.1))
#     for i in range(np.shape(matrix)[0]):
#         for j in range(np.shape(matrix)[1]):
#             if matrix[i][j] == 0:
#                 matrix[i][j] = float('nan')
#             else:
#                 matrix[i][j] = (i + 1)
#             if points_matrix[i][j] == 0:
#                 points_matrix[i][j] = float('nan')
#     print('d')
#     for i in range(np.shape(matrix)[0]):
#         plt.plot(plot_array, matrix[i][:], c='red')
#         plt.scatter(plot_array, points_matrix[i][:], 10,
#                     c='red')

#     plt.xlabel("Р’СЂРµРјСЏ")
#     plt.grid()
#     plt.ylabel("РљР°РЅР°Р»С‹")
#     plt.locator_params(axis='x', nbins=20)
#     plt.locator_params(axis='y', nbins=1)

#     plt.show()