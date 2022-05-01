import sort_types
from random import randint
from  time import time
from tkinter import Tk, Canvas

def time_sort(sp, _list):
    n = time()
    sp(_list.copy())
    k = time()
    return k-n

def rand_gen(n):
    return [randint(0,100000) for i in range(n)]

def center(dot):
    x, y = dot
    x *= cell_width / c_in_cell
    x += axis_x
    y *= cell_height * 10 / max_time
    y = axis_y - y
    return x, y

canvas_height = 640
canvas_width = 1040
cell_height = (canvas_height - 40) // 10
cell_width = (canvas_width - 40) // 10
axis_x = 20
axis_y = canvas_height - 20

step = 1000
_range = 20000
max_time = 1

c_in_cell = _range // 10
t_in_cell = max_time / 10

colors = {'bubble_sort':'red2', 'mod_bubble_sort':'lawn green', 'quick_sort':'purple',
          'selection_sort':'salmon', 'insert_sort':'khaki', 'shell_sort':'deep sky blue'}

root = Tk()
root.geometry('+0+0')

canvas = Canvas(height=canvas_height, width=canvas_width, background='snow')
canvas.pack()


canvas.create_text((axis_x-10, axis_y+10), text='0')

p = 0
for i in range(cell_width+axis_x, canvas_width+axis_x, cell_width):
    p += c_in_cell
    canvas.create_line((i, 0), (i, canvas_height), fill='grey60', dash=1)
    canvas.create_line((i, axis_y-3), (i, axis_y+3))
    canvas.create_text((i, axis_y+10), text=f'{p}')
canvas.create_line((axis_x, 0), (axis_x, canvas_height), arrow='first')
canvas.create_text((canvas_width-70, axis_y-10), text='размер массива', font=20)

p = 0
for i in range(axis_y-cell_height, 10-cell_height, -cell_height):
    p += t_in_cell
    canvas.create_line((0, i), (canvas_width, i), fill='grey60', dash=1)
    canvas.create_line((axis_x-3, i), (axis_x+3, i))
    canvas.create_text((axis_x-10, i), text=f'{round(p, 1)}')
canvas.create_line((0, axis_y), (canvas_width, axis_y), arrow='last')
canvas.create_text((axis_x+50, 20), text='время, сек', font=20)

types = {}
for i in [i for i in dir(sort_types) if 'sort' in i]:
    types[i] = [(0,0)]

for i, p in enumerate(types, 1):
    canvas.create_text((canvas_width-150, 20+i*40), text=f'{i}. {p}', font=('Times', 30), fill=colors[p])

root.update()

f = open('results-1.txt', 'w')
print(help(f))
for c in range(step, _range+1, step):
    temp = rand_gen(c)
    print(c)
    f.write(str(c)+'\n')
    for i in types:
        if types[i][-1][1] >= max_time:
            continue
        t = time_sort(eval('sort_types.'+i), temp)
        print(i, t)
        f.write(f'{i} {t}\n')
        types[i].append((c, t))
        canvas.create_line(center(types[i][-2]), center(types[i][-1]), fill=colors[i], width=2)
        canvas.update()
    print()
    f.write('\n')

f.truncate(f.tell()-2)
f.close()

root.mainloop()

with open('results-2.txt', 'w') as f:
    for i in types:
        f.write(i+'\n')
        for t in types[i][1:]:
            f.write(f'{t[0]} - {t[1]}\n')
        f.write('\n')
