from tkinter import Tk, Canvas, LabelFrame, Button, Label, Entry, Frame
from math import *

def get_text(w):
    if n := w.get():
        return n
    return '0'

def function(f, **kwargs):
    if f == '0':
        return ''
    if 'f' in f:
        return hard_function(f, kwargs)
    sp = []
    x = x_min
    while x <= x_max:
        sp.append((x, eval(f)))
        x = round(x + step, len_step)
    return tuple(sp)

def hard_function(f, kwargs):
    sp = []
    x = x_min
    i = 0
    while x <= x_max:
        if kwargs['f1']:
            f1 = kwargs['f1'][i][1]
        if kwargs['f2']:
            f2 = kwargs['f2'][i][1]
        sp.append((x, eval(f)))
        x = round(x + step, len_step)
        i += 1
    return tuple(sp)

def x_limits():
    global x_min, x_max
    x_min = eval(get_text(x_interval_start_entry))
    if x_min == 0:
        x_min = 0
    x_max = eval(get_text(x_interval_finish_entry))
    if x_max == 0:
        x_max = 1

def get_step():
    global step, len_step
    step = eval(get_text(step_entry))
    if step == 0:
        step = 1
    len_step = 0
    if '.' in str(step):
        n = str(step)
        len_step = len(n[n.find('.')+1:])

def y_limits(f1, f2, f3):
    global y_min, y_max
    y_min, y_max = 0, 0
    for i in range(len(f1)):
        y_min = min(y_min, f1[i][1])
        y_max = max(y_max, f1[i][1])
    for i in range(len(f2)):
        y_min = min(y_min, f2[i][1])
        y_max = max(y_max, f2[i][1])
    for i in range(len(f3)):
        y_min = min(y_min, f3[i][1])
        y_max = max(y_max, f3[i][1])

def cell_size():
    global cell_height, cell_width

    if x_min <= 0 <= x_max:
        xcount = round(x_max - x_min)
    elif x_max < 0:
        xcoun = round(-x_min)
    else:
        xcount = round(x_max)
    cell_width = canvas_width // (xcount + 2)

    if y_min <= 0 <= y_max:
        ycount = round(y_max - y_min)
    elif y_max < 0:
        ycount = round(-y_min)
    else:
        ycount = round(y_max)
    cell_height = canvas_height // (ycount + 2)

def axis_xy():
    global axis_x, axis_y

    if x_min <= 0 <= x_max:
        axis_x = (round(-x_min) + 1) * cell_width
    elif x_max < 0:
        axis_x = cell_width * (canvas_width // cell_width - 1)
    else:
        axis_x = cell_width

    if y_min <= 0 <= y_max:
        axis_y = (round(y_max) + 1) * cell_height
    elif y_max < 0:
        axis_y = cell_height
    else:
        axis_y = cell_height * (canvas_height // cell_height - 1)

def grid():
    for x in range(cell_width, canvas_width, cell_width):
        canvas.create_line((x, 0), (x, canvas_height), fill='grey70', dash=1)
        canvas.create_line((x, axis_y - 2), (x, axis_y + 2), fill='black')
    for y in range(cell_height, canvas_height, cell_height):
        canvas.create_line((0, y), (canvas_width, y), fill='grey70', dash=1)
        canvas.create_line((axis_x - 2, y), (axis_x + 2, y), fill='black')

def axis():
    canvas.create_line((0, axis_y), (canvas_width, axis_y), arrow='last')
    canvas.create_line((axis_x, 0), (axis_x, canvas_height), arrow='first')
    canvas.create_oval((axis_x-2, axis_y-2), (axis_x+2, axis_y+2), fill='black')

def text():
    canvas.create_text(axis_x + 10, axis_y - 10, text='0')

    if x_min <= -1:
        canvas.create_text(axis_x - cell_width, axis_y + 10, text='-1')
    if x_max >= 1:
        canvas.create_text(axis_x + cell_width, axis_y + 10, text='1')

    if y_min <= -1:
        canvas.create_text(axis_x + 10, axis_y + cell_height, text='-1')
    if y_max >= 1:
        canvas.create_text(axis_x + 10, axis_y - cell_height, text='1')

def center(dot):
    x, y = dot
    x *= cell_width
    x += axis_x
    y *= cell_height
    y = axis_y - y
    return x, y

def build(event=''):
    out.configure(text='Wait')
    out.update()
    try:
        canvas.delete('all')
        x_limits()
        get_step()
        f1 = function(get_text(f1_entry))
        f2 = function(get_text(f2_entry), f1=f1, f2=())
        f3 = function(get_text(f3_entry), f1=f1, f2=f2)
        y_limits(f1, f2, f3)
        cell_size()
        axis_xy()
        grid()
        axis()
        text()
        if f1 != '': canvas.create_line(tuple(map(center, f1)), width=line_width, fill='red')
        if f2 != '': canvas.create_line(tuple(map(center, f2)), width=line_width, fill='green')
        if f3 != '': canvas.create_line(tuple(map(center, f3)), width=line_width, fill='blue')
        out.configure(text='Done')
    except Exception as e:
        out.configure(text=f'{e}')
        raise e

root = Tk()
root.geometry('+0+0')

canvas_height = 400
canvas_width = 800
line_width = 2
axis_x, axis_y = 0, 0
x_min, x_max, y_min, y_max = 0, 0, 0, 0
cell_height, cell_width = 0, 0
step = 0

canvas = Canvas(height=canvas_height, width=canvas_width, background='snow')
canvas.pack()

frame = LabelFrame(text='Functions')

Label(frame, text='f1', font='Times 30', fg='red').pack(side='left', padx=5, pady=5)
f1_entry = Entry(frame, font='Times 30', width=10, fg='red')
f1_entry.pack(side='left', padx=5, pady=5)

Label(frame, text='f2', font='Times 30', fg='green').pack(side='left', padx=5, pady=5)
f2_entry = Entry(frame, font='Times 30', width=10, fg='green')
f2_entry.pack(side='left', padx=5, pady=5)

Label(frame, text='f3', font='Times 30', fg='blue').pack(side='left', padx=5, pady=5)
f3_entry = Entry(frame, font='Times 30', width=10, fg='blue')
f3_entry.pack(side='left', padx=5, pady=5)

frame.pack(pady=5)

frame2 = Frame()
interval_frame = LabelFrame(frame2, text='Interval')

x_interval_start_entry = Entry(interval_frame, font='Times 30', width=5)
x_interval_start_entry.pack(side='left', padx=5, pady=5)
Label(interval_frame, text='≤ x ≤', font='Times 30').pack(side='left', padx=5, pady=5)
x_interval_finish_entry = Entry(interval_frame, font='Times 30', width=5)
x_interval_finish_entry.pack(side='left', padx=5, pady=5)

interval_frame.pack(side='left', padx=30)

Label(frame2, text='Step', font=('Times', 30)).pack(side='left', padx=10)
step_entry = Entry(frame2, font='Times 30', width=5)
step_entry.pack(side='left')

Button(frame2, text='PRINT', font=('Times', 30), command=build).pack(side='left', padx=20)
root.bind('<Return>', build)

frame2.pack()

out = Label(text='|\t-\t-\t-\t-\t-\t|', font=('Times', 20), width=50)
out.pack()

root.mainloop()
