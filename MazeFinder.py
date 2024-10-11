import tkinter
from tkinter import *
import time
# import dijkstar
import math

window = Tk()
Width = 1600
Height = 900
window.geometry("1600x900")  # resolution of the window (my screen max = 1600 x 900)
repeat_time = 0  # time a map can be duplicated (with my screen is 2)
flag = 0  # 0 = Start Point, 1 = End Point
stor = []  # storing vertices of the graphs
visib = []  # storing edges of the visibility graphs
svisib = []  # storing edges of the visibility graphs with spoint
evisib = []  # storing edges of the visibility graphs with epoint
total = []  # storing edges of the final graphs
spoint = [0, 0]  # starting point
epoint = [0, 0]  # ending point
ShortestPath = []  # storing edges of the Shortest Point
checkrepeat = 0
flag_cleared = 0
flag_drawn_visib = 0
flag_drawn_svisib = 0
flag_drawn_evisib = 0
flag_calculated = 0
x_changed = 0
y_changed = 0
sx_changed, sy_changed = 0, 0
ex_changed, ey_changed = 0, 0

# top_list1 = vertices of the original 1st graph
top_list1 = [[0, 0], [1, 0], [1, 8], [2, 8], [2, 0], [5, 0], [5, 1], [3, 1], [3, 4], [5, 4], [5, 5], [3, 5], [3, 8],
             [6, 8], [6, 0], [9, 0], [9, 1], [7, 1], [7, 4], [9, 4], [9, 5], [7, 5], [7, 8], [9, 8], [9, 9], [8, 9],
             [0, 9], [0, 1], [0, 0]]

# Translation by x amount
for i in range(len(top_list1)):
    top_list1[i][1] += 2
    top_list1[i][0] += 2

my_canvas = Canvas(window, width=Width, height=Height, bg="gray")

grid_slider = Scale(window, from_=1, to=99, orient=HORIZONTAL)
grid_slider.pack(anchor=W)
lb1 = Label(window, text="Grid Size")
lb1.pack(anchor=W)
repeat_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL)
repeat_slider.pack(anchor=W)
lb2 = Label(window, text="Repeat Time")
lb2.pack(anchor=W)

# Scrolling
scroll_vert = Scale(window, from_=0, to=100, length=100)
scroll_vert.place(x=1301, y=12)
lb3 = Label(window, text="Vertical")
lb3.place(x=1314, y=110)
scroll_hori = Scale(window, from_=0, to=100, length=100)
scroll_hori.place(x=1231, y=12)
lb4 = Label(window, text="Horizontal")
lb4.place(x=1236, y=110)

lb5 = Label(window, text="Runtime Visib: ", font=20)
lb5.place(x=800, y=18)
lb6 = Label(window, text="Runtime Shortest: ", font=20)
lb6.place(x=800, y=53)
lb7 = Label(window, text="Distance: ", font=20)
lb7.place(x=800, y=90)

# Button to draw Visibility Graphs
Btn_Visib_Graphs = Button(window, text="Visibility Graphs", bd='5')
Btn_Visib_Graphs.place(x=225, y=45)

# Button to generate start point
Btn_start_point = Button(window, text="Start Point", bd='5')
Btn_start_point.place(x=110, y=10)

# Button to generate end point
Btn_end_point = Button(window, text="End Point", bd='5')
Btn_end_point.place(x=110, y=80)

# Button to calculate the shortest distance from start point to end point (using Dijkstra)
Btn_cal = Button(window, text="Calculate", bd='5')
Btn_cal.place(x=495, y=45)

# Button to clear shortest path
Btn_clear_Path = Button(window, text="Clear Path", bd='5')
Btn_clear_Path.place(x=600, y=45)

# Button to show Visibility Graphs
Btn_show_visib = Button(window, text="Show Visib", bd='5')
Btn_show_visib.place(x=375, y=0)

# Button to show Visibility Graphs for Start point
Btn_show_svisib = Button(window, text="Show SVisib", bd='5')
Btn_show_svisib.place(x=375, y=45)

# Button to show Visibility Graphs for End point
Btn_show_evisib = Button(window, text="Show EVisib", bd='5')
Btn_show_evisib.place(x=375, y=90)

# Distance between grids
grid_size = 38


def ClearShortestPath():
    global flag_cleared, flag_calculated
    my_canvas.delete("dijk")
    flag_cleared = 1
    flag_calculated = 0


def creategrids(gz):
    global spoint, epoint, grid_size, checkrepeat, ShortestPath, stor, flag_cleared, y_changed, x_changed
    global flag_drawn_visib, flag_drawn_svisib, flag_drawn_evisib, flag_calculated
    my_canvas.delete("blue")
    my_canvas.delete("green")
    if checkrepeat == 0:
        my_canvas.delete("dijk")
    spoint = (spoint[0] / grid_size, spoint[1] / grid_size)
    epoint = (epoint[0] / grid_size, epoint[1] / grid_size)
    my_canvas.delete("grid")
    grid_size = int(gz)
    spoint = (spoint[0] * grid_size, spoint[1] * grid_size)
    epoint = (epoint[0] * grid_size, epoint[1] * grid_size)
    create_circle(spoint[0] + (sx_changed - x_changed) * grid_size, spoint[1] + (sy_changed - y_changed) * grid_size, 4,
                  "blue")
    create_circle(epoint[0] + (ex_changed - x_changed) * grid_size, epoint[1] + (ey_changed - y_changed) * grid_size, 4,
                  "green")
    # spoint[1] = spoint[1] / grid_size
    i = 0
    while i <= max(Width, Height):
        my_canvas.create_line(0, i, Width, i, tags="grid")
        my_canvas.create_line(i, 0, i, Height, tags="grid")
        i = i + grid_size
    my_canvas.delete("map1")
    # global stor
    stor = []
    p = 1
    stor.append([top_list1[0][0] - x_changed, top_list1[0][1] - y_changed])
    while p <= repeat_time:
        if p == 1:
            l = 0
        else:
            l = 1
        for i in range(l, 23):
            my_canvas.create_line((top_list1[i][0] + 8 * (p - 1) - x_changed) * grid_size,
                                  (top_list1[i][1] + 8 * (p - 1) - y_changed) * grid_size,
                                  (top_list1[i + 1][0] + 8 * (p - 1) - x_changed) * grid_size,
                                  (top_list1[i + 1][1] + 8 * (p - 1) - y_changed) * grid_size,
                                  fill="lightblue", width=3, tags="map1")
            stor.append([top_list1[i + 1][0] + 8 * (p - 1) - x_changed, top_list1[i + 1][1] + 8 * (p - 1) - y_changed])
        p += 1
    p -= 1
    my_canvas.create_line((top_list1[23][0] + 8 * (p - 1) - x_changed) * grid_size,
                          (top_list1[23][1] + 8 * (p - 1) - y_changed) * grid_size,
                          (top_list1[24][0] + 8 * (p - 1) - x_changed) * grid_size,
                          (top_list1[24][1] + 8 * (p - 1) - y_changed) * grid_size,
                          fill="lightblue", width=3, tags="map1")
    stor.append([top_list1[24][0] + 8 * (p - 1) - x_changed, top_list1[24][1] + 8 * (p - 1) - y_changed])
    while p >= 1:
        if p == repeat_time:
            l = 24
        else:
            l = 25
        while l <= 26:
            if (p == repeat_time and l == 24) or (p == 1 and l == 26):
                my_canvas.create_line((top_list1[l][0] + 8 * (p - 1) - x_changed) * grid_size,
                                      (top_list1[l][1] + 8 * (p - 1) - y_changed) * grid_size,
                                      (top_list1[l + 2][0] + 8 * (p - 1) - x_changed) * grid_size,
                                      (top_list1[l + 2][1] + 8 * (p - 1) - y_changed) * grid_size,
                                      fill="lightblue", width=3, tags="map1")
                stor.append(
                    [top_list1[l + 2][0] + 8 * (p - 1) - x_changed, top_list1[l + 2][1] + 8 * (p - 1) - y_changed])
                l += 2
            else:
                my_canvas.create_line((top_list1[l][0] + 8 * (p - 1) - x_changed) * grid_size,
                                      (top_list1[l][1] + 8 * (p - 1) - y_changed) * grid_size,
                                      (top_list1[l + 1][0] + 8 * (p - 1) - x_changed) * grid_size,
                                      (top_list1[l + 1][1] + 8 * (p - 1) - y_changed) * grid_size,
                                      fill="lightblue", width=3, tags="map1")
                stor.append(
                    [top_list1[l + 1][0] + 8 * (p - 1) - x_changed, top_list1[l + 1][1] + 8 * (p - 1) - y_changed])
                l += 1
        p -= 1
    if flag_cleared == 0:
        for i in range(len(ShortestPath) - 1):
            my_canvas.create_line((ShortestPath[i][0] - x_changed) * grid_size,
                                  (ShortestPath[i][1] - y_changed) * grid_size,
                                  (ShortestPath[i + 1][0] - x_changed) * grid_size,
                                  (ShortestPath[i + 1][1] - y_changed) * grid_size,
                                  fill="pink", width=3, tags="dijk")
    if flag_drawn_visib == 1:
        my_canvas.delete("Visib")
        p = 1
        while p <= repeat_time:
            for i in range(len(visib)):
                if (p < repeat_time and visib[i][2] == 11 and visib[i][3] == 11) or \
                        (p > 1 and visib[i][0] == 2 and visib[i][1] == 2) or \
                        (p == 1 and visib[i][2] == 2 and visib[i][3] == 3) or \
                        (p == repeat_time and visib[i][2] == 10 and visib[i][3] == 11):
                    continue
                else:
                    my_canvas.create_line((visib[i][0] + 8 * (p - 1) - x_changed) * grid_size,
                                          (visib[i][1] + 8 * (p - 1) - y_changed) * grid_size,
                                          (visib[i][2] + 8 * (p - 1) - x_changed) * grid_size,
                                          (visib[i][3] + 8 * (p - 1) - y_changed) * grid_size,
                                          fill="pink", width=1, tags="Visib")
            p += 1
    if flag_drawn_svisib == 1:
        my_canvas.delete("SVisib")
        for i in range(len(svisib)):
            my_canvas.create_line((stor[svisib[i][1] + flag_calculated][0]) * grid_size,
                                  (stor[svisib[i][1] + flag_calculated][1]) * grid_size,
                                  spoint[0] + (sx_changed - x_changed) * grid_size, spoint[1] + (sy_changed - y_changed) * grid_size, fill='blue',
                                  width='1', tags="SVisib")
    if flag_drawn_evisib == 1:
        my_canvas.delete("EVisib")
        for i in range(len(evisib)):
            my_canvas.create_line((stor[evisib[i][1] + flag_calculated][0]) * grid_size,
                                  (stor[evisib[i][1] + flag_calculated][1]) * grid_size,
                                  epoint[0] + (ex_changed - x_changed) * grid_size, epoint[1] + (ey_changed - y_changed) * grid_size, fill='green',
                                  width='1', tags="EVisib")


def changerepeattime(rp):
    global repeat_time
    global checkrepeat
    repeat_time = int(rp)
    checkrepeat = 1
    creategrids(int(grid_slider.get()))
    checkrepeat = 0


def changescrollvert(yc):
    global y_changed
    y_changed = int(yc)
    creategrids(int(grid_slider.get()))


def changescrollhori(xc):
    global x_changed
    x_changed = int(xc)
    creategrids(int(grid_slider.get()))


def create_circle(x, y, r, str):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return my_canvas.create_oval(x0, y0, x1, y1, fill=str, tags=str)


def Start_Point():
    global flag
    flag = 0
    my_canvas.bind("<Button-1>", draw_line)


def End_Point():
    global flag
    flag = 1
    my_canvas.bind("<Button-1>", draw_line)


def draw_line(e):
    global spoint, epoint, svisib, evisib
    global sx_changed, sy_changed, ex_changed, ey_changed
    global x_changed, y_changed
    x, y = e.x, e.y
    if flag == 0 and in_polygon(x, y):
        spoint = [x, y]
        sx_changed = x_changed
        sy_changed = y_changed
        my_canvas.delete("blue")
        my_canvas.delete("spoint")
        svisib = []
        creategrids(int(grid_slider.get()))
        create_circle(x, y, 4, "blue")
    if flag == 1 and in_polygon(x, y):
        epoint = [x, y]
        ex_changed = x_changed
        ey_changed = y_changed
        my_canvas.delete("green")
        my_canvas.delete("epoint")
        evisib = []
        creategrids(int(grid_slider.get()))
        create_circle(x, y, 4, "green")
    # check_both_points()


def check_both_points():
    global spoint
    global epoint
    if in_polygon(spoint[0], spoint[1]) and in_polygon(epoint[0], epoint[1]):
        print("BOTH POINTS IN POLYGON")
    else:
        print("EITHER ONE POINT IS OUTSIDE POLYGON")


my_canvas.pack()


my_canvas.old_coords = None
def in_polygon(x, y):
    global stor
    inside = False
    for u in range(0, len(stor) - 1):
        xu = stor[u][0] * grid_size
        yv = stor[u][1] * grid_size
        xv = stor[u + 1][0] * grid_size
        yu = stor[u + 1][1] * grid_size

        if yv > yu:
            xu, xv = xv, xu
            yv, yu = yu, yv

        if yv < y <= yu and x <= xu + (xv - xu) * (y - yv) / (yu - yv):
            inside = not inside

    # print(len(stor))
    return inside


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) >= (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def VisibilityGraph():
    # print(repeat_time)
    global stor, spoint, epoint, svisib, evisib, total, visib
    global x_changed, y_changed, sx_changed, sy_changed, ex_changed, ey_changed
    total, visib = [], []
    start = time.time()
    for i in range(len(top_list1) - 1):
        for j in range(i + 2, len(top_list1) + i - 2):
            f = 0
            if top_list1[i][0] == top_list1[j % len(top_list1)][0] and abs(top_list1[i][1] - top_list1[j % len(top_list1)][1]) == 1 or \
               top_list1[i][1] == top_list1[j % len(top_list1)][1] and abs(top_list1[i][0] - top_list1[j % len(top_list1)][0]) == 1:
                if in_polygon((top_list1[i][0] + top_list1[j % len(top_list1)][0] - 2 * x_changed) / 2 * grid_size,
                              (top_list1[i][1] + top_list1[j % len(top_list1)][1] - 2 * y_changed) / 2 * grid_size):
                    f = 1
            if (f == 0) and (top_list1[i][0] == top_list1[j % len(top_list1)][0] or top_list1[i][1] ==
                             top_list1[j % len(top_list1)][1] or
                             not in_polygon(
                                 (top_list1[i][0] + top_list1[j % len(top_list1)][0] - 2 * x_changed) / 2 * grid_size,
                                 (top_list1[i][1] + top_list1[j % len(top_list1)][1] - 2 * y_changed) / 2 * grid_size)):
                continue
            cnt = 0
            # else:
            for x in range(len(top_list1) - 1):
                if not intersect(top_list1[i], top_list1[j % len(top_list1)], top_list1[x], top_list1[x + 1]) \
                        or top_list1[i] == top_list1[x] \
                        or top_list1[i] == top_list1[x + 1] \
                        or top_list1[j % len(top_list1)] == top_list1[x] \
                        or top_list1[j % len(top_list1)] == top_list1[x + 1]:
                    cnt += 1
            if cnt == len(top_list1) - 1:
                if not ([top_list1[j % len(top_list1)][0], top_list1[j % len(top_list1)][1], top_list1[i][0],
                         top_list1[i][1]]) in visib:
                    visib.append([top_list1[i][0], top_list1[i][1], top_list1[j % len(top_list1)][0],
                                  top_list1[j % len(top_list1)][1]])
    # print(visib)
    p = 1
    # print(stor)
    while p <= repeat_time:
        for i in range(len(visib)):
            if (p < repeat_time and visib[i][2] == 11 and visib[i][3] == 11) or \
                    (p > 1 and visib[i][0] == 2 and visib[i][1] == 2) or \
                    (p == 1 and visib[i][2] == 2 and visib[i][3] == 3) or \
                    (p == repeat_time and visib[i][2] == 10 and visib[i][3] == 11):
                continue
            else:
                # print(1)
                #print(visib[i][0] + 8 * (p - 1) - x_changed, visib[i][1] + 8 * (p - 1) - y_changed,
                #      visib[i][2] + 8 * (p - 1) - x_changed, visib[i][3] + 8 * (p - 1) - y_changed)
                total.append(
                    [stor.index([visib[i][0] + 8 * (p - 1) - x_changed, visib[i][1] + 8 * (p - 1) - y_changed]) + 2 ,
                     stor.index([visib[i][2] + 8 * (p - 1) - x_changed, visib[i][3] + 8 * (p - 1) - y_changed]) + 2,
                     math.sqrt((visib[i][2] - visib[i][0]) ** 2 + (visib[i][3] - visib[i][1]) ** 2)])
        p += 1
    # print(stor)
    # print(total)
    # Drawing visibility graphs with spoint
    # print(stor)
    if spoint != [0, 0]:
        tempx = (spoint[0] / grid_size)
        tempy = (spoint[1] / grid_size)
        tempx += (sx_changed - x_changed)
        tempy += (sy_changed - y_changed)
        temp = [tempx, tempy]
        cnt = 0
        while tempx - 8 * cnt >= 2 - x_changed and tempy - 8 * cnt >= 2 - y_changed:
            cnt += 1
        if 10 - x_changed <= tempx - 8 * (cnt - 2) <= 11 - y_changed and \
           10 - x_changed <= tempy - 8 * (cnt - 2) <= 11 - y_changed and cnt >= 2:
            k = 8 * (cnt - 2)
            for i in range(len(top_list1) - 1):
                if top_list1[i][0] + k - x_changed == tempx and abs(top_list1[i][1] + k - y_changed - tempy) <= 1 or \
                   top_list1[i][1] + k - y_changed == tempy and abs(top_list1[i][0] + k - y_changed - tempx) <= 1:
                    if in_polygon((top_list1[i][0] + k - x_changed + tempx) / 2 * grid_size,
                                  (top_list1[i][1] + k - y_changed + tempy) / 2 * grid_size):
                        i = i
                elif top_list1[i][0] + k - x_changed == tempx or top_list1[i][1] + k - y_changed == tempy or (
                        top_list1[i] == [11, 11] and cnt < repeat_time + 1) or (
                        top_list1[i] == [10, 11] and cnt == repeat_time + 1):
                    continue
                p = 0
                for x in range(len(top_list1) - 1):
                    if (not intersect([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed], temp,
                                      [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed],
                                      [top_list1[x + 1][0] + k - x_changed, top_list1[x + 1][1] + k - y_changed])
                        or (top_list1[i] == top_list1[x])
                        or (top_list1[i] == top_list1[x + 1])
                        or (temp == [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed])
                        or (temp == [top_list1[x + 1][0] + k - x_changed, top_list1[x][1] + k - y_changed])) \
                            and in_polygon((top_list1[i][0] - x_changed + k + tempx) / 2 * grid_size,
                                           (top_list1[i][1] - y_changed + k + tempy) / 2 * grid_size):
                        p += 1
                if p == len(top_list1) - 1:
                    if not ([stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed]), len(stor)]) in visib:
                        svisib.append([len(stor), stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed])])
                    # print(1)
        # print(svisib)
        print(stor)
        k = 8 * (cnt - 1)
        for i in range(len(top_list1) - 1):
            if top_list1[i][0] + k - x_changed == tempx and abs(top_list1[i][1] + k - y_changed - tempy) <= 1 or \
               top_list1[i][1] + k - y_changed == tempy and abs(top_list1[i][0] + k - x_changed - tempx) <= 1:
                if in_polygon((top_list1[i][0] - x_changed + k + tempx) / 2 * grid_size,
                              (top_list1[i][1] - y_changed + k + tempy) / 2 * grid_size):
                    i = i
            elif top_list1[i][0] + k - x_changed == tempx or top_list1[i][1] + k - y_changed == tempy or (
                    top_list1[i] == [2, 3] and (cnt == 1 or cnt == repeat_time + 1)) or (
                    top_list1[i] == [2, 2] and cnt > 1) or (top_list1[i] == [10, 11] and cnt == repeat_time) or (
                    top_list1[i] == [11, 11] and cnt < repeat_time + 1):
                continue
            p = 0
            for x in range(len(top_list1) - 1):
                if (not intersect([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed], temp,
                                  [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed],
                                  [top_list1[x + 1][0] + k - x_changed, top_list1[x + 1][1] + k - y_changed])
                    or (top_list1[i] == top_list1[x])
                    or (top_list1[i] == top_list1[x + 1])
                    or (temp == [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed])
                    or (temp == [top_list1[x + 1][0] + k - x_changed, top_list1[x + 1][1] + k - y_changed])) \
                        and in_polygon((top_list1[i][0] - x_changed + k + tempx) / 2 * grid_size,
                                       (top_list1[i][1] - y_changed + k + tempy) / 2 * grid_size):
                    p += 1
            if p == len(top_list1) - 1:
                if not ([stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed]), len(stor)]) in visib:
                    svisib.append([len(stor), stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed])])
        # print(svisib)
    # Drawing visibility graphs with epoint
    if epoint != [0, 0]:
        evisib = []
        tempx = (epoint[0] / grid_size)
        tempy = (epoint[1] / grid_size)
        tempx += (ex_changed - x_changed)
        tempy += (ey_changed - y_changed)
        temp = [tempx, tempy]
        cnt = 0
        while tempx - 8 * cnt >= 2 - x_changed and tempy - 8 * cnt >= 2 - y_changed:
            cnt += 1
            # print(cnt)
        if 10 - x_changed <= tempx - 8 * (cnt - 2) <= 11 - y_changed and \
           10 - x_changed <= tempy - 8 * (cnt - 2) <= 11 - y_changed and cnt >= 2:
            k = 8 * (cnt - 2)
            for i in range(len(top_list1) - 1):
                if top_list1[i][0] + k - x_changed == tempx and abs(top_list1[i][1] + k - y_changed - tempy) <= 1 or \
                   top_list1[i][1] + k - y_changed == tempy and abs(top_list1[i][0] + k - x_changed - tempx) <= 1:
                    if in_polygon((top_list1[i][0] + k - x_changed + tempx) / 2 * grid_size,
                                  (top_list1[i][1] + k - y_changed + tempy) / 2 * grid_size):
                        i = i
                elif top_list1[i][0] + k - x_changed == tempx or top_list1[i][1] + k - y_changed == tempy or (
                        top_list1[i] == [11, 11] and cnt < repeat_time + 1) or (
                        top_list1[i] == [10, 11] and cnt == repeat_time + 1):
                    continue
                p = 0
                for x in range(len(top_list1) - 1):
                    if (not intersect([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed], temp,
                                      [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed],
                                      [top_list1[x + 1][0] + k - x_changed, top_list1[x + 1][1] + k - y_changed])
                        or (top_list1[i] == top_list1[x])
                        or (top_list1[i] == top_list1[x + 1])
                        or (temp == [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed])
                        or (temp == [top_list1[x + 1][0] + k - x_changed, top_list1[x][1] + k - y_changed])) \
                            and in_polygon((top_list1[i][0] + k - x_changed + tempx) / 2 * grid_size,
                                           (top_list1[i][1] + k - y_changed + tempy) / 2 * grid_size):
                        p += 1
                if p == len(top_list1) - 1:
                    if not ([stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed]), len(stor) + 1]) in visib:
                        evisib.append([len(stor) + 1, stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed])])
                        # print(1)
        k = 8 * (cnt - 1)
        for i in range(len(top_list1) - 1):
            if top_list1[i][0] + k - x_changed == tempx and abs(top_list1[i][1] + k - x_changed - tempy) <= 1 or \
               top_list1[i][1] + k - y_changed == tempy and abs(top_list1[i][0] + k - y_changed - tempx) <= 1:
                if in_polygon((top_list1[i][0] + k - x_changed + tempx) / 2 * grid_size,
                              (top_list1[i][1] + k - y_changed + tempy) / 2 * grid_size):
                    i = i
            elif top_list1[i][0] + k - x_changed == tempx or top_list1[i][1] + k - y_changed == tempy or (
                 top_list1[i] == [2, 3] and (cnt == 1 or cnt == repeat_time + 1)) or (
                 top_list1[i] == [2, 2] and cnt > 1) or (top_list1[i] == [10, 11] and cnt == repeat_time) or (
                 top_list1[i] == [11, 11] and cnt < repeat_time + 1):
                continue
            p = 0
            for x in range(len(top_list1) - 1):
                if (not intersect([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed], temp,
                                  [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed],
                                  [top_list1[x + 1][0] + k - x_changed, top_list1[x + 1][1] + k - y_changed])
                    or (top_list1[i] == top_list1[x])
                    or (top_list1[i] == top_list1[x + 1])
                    or (temp == [top_list1[x][0] + k - x_changed, top_list1[x][1] + k - y_changed])
                    or (temp == [top_list1[x + 1][0] + k - x_changed, top_list1[x + 1][1] + k - y_changed])) \
                        and in_polygon((top_list1[i][0] + k - x_changed + tempx) / 2 * grid_size,
                                       (top_list1[i][1] + k - y_changed + tempy) / 2 * grid_size):
                    p += 1
            if p == len(top_list1) - 1:
                if not ([stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed]), len(stor) + 1]) in visib:
                    evisib.append([len(stor) + 1, stor.index([top_list1[i][0] + k - x_changed, top_list1[i][1] + k - y_changed])])
    end = time.time()
    print(end - start)
    lb5.configure(text=("Runtime Visib: " + str((end - start))))


# Draw Visibility Graph
def Dijkstra():
    global visib, svisib, evisib, spoint, epoint, total, ShortestPath, flag_cleared, flag_calculated
    global sx_changed, sy_changed, ex_changed, ey_changed, x_changed, y_changed
    flag_cleared = 0
    flag_calculated = 2
    a, w, d, trace = [], [], [], []
    n = len(stor)
    start = time.time()
    stor.insert(0, [epoint[0] / grid_size + (ex_changed - x_changed), epoint[1] / grid_size + (ey_changed - y_changed)])
    stor.insert(0, [spoint[0] / grid_size + (sx_changed - x_changed), spoint[1] / grid_size + (sy_changed - y_changed)])
    for i in range(n - 1):
        total.append(
            [i + 2, i + 3, math.sqrt((stor[i + 2][0] - stor[i + 3][0]) ** 2 + (stor[i + 2][1] - stor[i + 3][1]) ** 2)])
    for i in range(len(evisib)):
        total.append([evisib[i][1] + 2, 1, math.sqrt((epoint[0] / grid_size + (ex_changed - x_changed) - stor[evisib[i][1] + 2][0]) ** 2 + (
                epoint[1] / grid_size + (ey_changed - y_changed) - stor[evisib[i][1] + 2][1]) ** 2)])
    for i in range(len(svisib)):
        total.append([0, svisib[i][1] + 2, math.sqrt((spoint[0] / grid_size + (sx_changed - x_changed) - stor[svisib[i][1] + 2][0]) ** 2 + (
                spoint[1] / grid_size + (sy_changed - y_changed) - stor[svisib[i][1] + 2][1]) ** 2)])
    # print(total)
    for i in range(n + 2):
        a.append(False)
        d.append(round(1e18))
        w.append([])
        trace.append(0)
    for i in range(len(total)):
        w[total[i][0]].append([total[i][1], total[i][2]])
        w[total[i][1]].append([total[i][0], total[i][2]])
    # print(w[0])
    d[0] = 0
    for i in range(0, n + 2):
        ubest = 0
        Max = round(1e18)
        for u in range(0, n + 2):
            if d[u] < Max and not a[u]:
                ubest = u
                Max = d[u]
        u = ubest
        a[u] = True
        for x in range(len(w[u])):
            v = w[u][x][0]
            we = w[u][x][1]
            if d[v] > d[u] + we:
                d[v] = d[u] + we
                trace[v] = u
    ShortestPath = []
    curr = 1
    coordcurr = stor[curr]
    ShortestPath.append(coordcurr)
    while curr != 0:
        curr = trace[curr]
        ShortestPath.append(stor[curr])
        my_canvas.create_line(coordcurr[0] * grid_size, coordcurr[1] * grid_size,
                              stor[curr][0] * grid_size, stor[curr][1] * grid_size,
                              fill="pink", width=3, tags="dijk")
        coordcurr = stor[curr]
    end = time.time()
    print(end - start)
    lb6.configure(text=("Runtime Shortest: " + str((end - start))))
    print(d[1])
    lb7.configure(text=("Distance: " + str(d[1])))


def DrawVisib():
    global visib, flag_drawn_visib, x_changed, y_changed
    if flag_drawn_visib == 0:
        p = 1
        while p <= repeat_time:
            for i in range(len(visib)):
                if (p < repeat_time and visib[i][2] == 11 and visib[i][3] == 11) or \
                        (p > 1 and visib[i][0] == 2 and visib[i][1] == 2) or \
                        (p == 1 and visib[i][2] == 2 and visib[i][3] == 3) or \
                        (p == repeat_time and visib[i][2] == 10 and visib[i][3] == 11):
                    continue
                else:
                    my_canvas.create_line((visib[i][0] + 8 * (p - 1) - x_changed) * grid_size,
                                          (visib[i][1] + 8 * (p - 1) - y_changed) * grid_size,
                                          (visib[i][2] + 8 * (p - 1) - x_changed) * grid_size,
                                          (visib[i][3] + 8 * (p - 1) - y_changed) * grid_size,
                                          fill="pink", width=1, tags="Visib")
            p += 1
            Btn_show_visib.configure(text="Remove Visib")
            flag_drawn_visib = 1
    elif flag_drawn_visib == 1:
        my_canvas.delete("Visib")
        Btn_show_visib.configure(text="Show Visib")
        flag_drawn_visib = 0


def DrawSVisib():
    global svisib, flag_drawn_svisib, stor, spoint, x_changed, y_changed, flag_calculated
    if flag_drawn_svisib == 0:
        for i in range(len(svisib)):
            my_canvas.create_line((stor[svisib[i][1] + flag_calculated][0] - x_changed) * grid_size,
                                  (stor[svisib[i][1] + flag_calculated][1] - y_changed) * grid_size,
                                  spoint[0] + (sx_changed - x_changed) * grid_size, spoint[1] + (sy_changed - y_changed) * grid_size, fill='blue',
                                  width='1', tags="SVisib")
        Btn_show_svisib.configure(text="Remove SVisib")
        flag_drawn_svisib = 1
        Btn_cal.place(x=515, y=45)
        Btn_clear_Path.place(x=620, y=45)
    elif flag_drawn_svisib == 1:
        my_canvas.delete("SVisib")
        Btn_show_svisib.configure(text="Show SVisib")
        flag_drawn_svisib = 0
        Btn_cal.place(x=500, y=45)
        Btn_clear_Path.place(x=605, y=45)


def DrawEVisib():
    global evisib, flag_drawn_evisib, stor, epoint
    if flag_drawn_evisib == 0:
        for i in range(len(evisib)):
            my_canvas.create_line((stor[evisib[i][1] + flag_calculated][0]) * grid_size,
                                  (stor[evisib[i][1] + flag_calculated][1]) * grid_size,
                                  epoint[0] + (ex_changed - x_changed) * grid_size, epoint[1] + (ey_changed - y_changed) * grid_size, fill='green',
                                  width='1', tags="EVisib")
        Btn_show_evisib.configure(text="Remove SVisib")
        flag_drawn_evisib = 1
    elif flag_drawn_evisib == 1:
        my_canvas.delete("EVisib")
        Btn_show_evisib.configure(text="Show EVisib")
        flag_drawn_evisib = 0


Btn_Visib_Graphs.configure(command=VisibilityGraph)


# my_canvas.create_line(-100, -100, 100, 100, fill="red", width=5)
Btn_start_point.configure(command=Start_Point)
Btn_end_point.configure(command=End_Point)
Btn_cal.configure(command=Dijkstra)
Btn_show_visib.configure(command=DrawVisib)
Btn_show_svisib.configure(command=DrawSVisib)
Btn_show_evisib.configure(command=DrawEVisib)
Btn_clear_Path.configure(command=ClearShortestPath)
grid_slider.configure(command=creategrids)
repeat_slider.configure(command=changerepeattime)
scroll_vert.configure(command=changescrollvert)
scroll_hori.configure(command=changescrollhori)
window.mainloop()