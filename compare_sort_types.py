import sort_types
from sort_types import *
from random import randint
from  time import time
from tkinter import Tk, Canvas

def time_sort(sp, _list):
    if types[sp][-1][1] >= 1:
        return 1
    n = time()
    eval(sp)(_list.copy())
    k = time()
    return k-n

def rand_gen(n):
    return [randint(0,100000) for i in range(n)]

def center(dot):
    x, y = dot
    x *= cell_width / 2000
    x += axis_x
    y *= cell_height * 10
    y = axis_y - y
    return x, y

canvas_height = 610
canvas_width = 1410
c_in_cell = 500
cell_height = (canvas_height - 10) // 10
cell_width = (canvas_width - 10) // 10
axis_x = 10
axis_y = canvas_height - 10

step = 100
_range = 20000

colors = {'bubble_sort':'red2', 'mod_bubble_sort':'lawn green', 'quick_sort':'purple',
          'selection_sort':'salmon', 'insert_sort':'khaki', 'shell_sort':'deep sky blue'}

root = Tk()

canvas = Canvas(height=canvas_height, width=canvas_width, background='snow')
canvas.pack()

for i in range(cell_width+10, canvas_width, cell_width):
    canvas.create_line((i, 0), (i, canvas_height), fill='grey60', dash=1)
canvas.create_line((10, 0), (10, canvas_height), arrow='first')

for i in range(cell_height, canvas_height-10, cell_height):
    canvas.create_line((0, i), (canvas_width, i), fill='grey60', dash=1)
canvas.create_line((0, canvas_height-10), (canvas_width, canvas_height-10), arrow='last')

types = {}
for i in [i for i in dir(sort_types) if 'sort' in i]:
    types[i] = [(0,0)]

for i, p in enumerate(types, 1):
    canvas.create_text((canvas_width-150, 20+i*40), text=f'{i}. {p}', font=('Times', 30), fill=colors[p])

root.update()

for c in range(step, _range+1, step):
    temp = rand_gen(c)
    print(c)
    for i in types:
        if types[i][-1][1] == 1:
            continue
        t = time_sort(i, temp)
        print(i, t)
        types[i].append((c, t))
        canvas.create_line(center(types[i][-2]), center(types[i][-1]), fill=colors[i], width=2)
        canvas.update()
root.mainloop()
