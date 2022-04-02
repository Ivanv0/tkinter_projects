from tkinter import Tk, Canvas
from math import pi, sqrt, sin, cos

# Функция смещения координат относитльно центра
# + перевод в декартову систему
def center(dot):
	x, y = dot
	x *= cell_w
	x += cx
	y *= cell_h
	y = cy - y
	return (x, y)

# Возвращает кортеж из точек по функции
def function(f):
	sp = []
	x = np
	while x < cp:
		sp.append((x, eval(f)))
		x += step
	return tuple(sp)

cell_h = 40 # высота клетки
cell_w = 100 # ширина клетки
ch = cell_h * 14 # общая высота canvas
cw = cell_w * 8 # общая ширина canvas
np = 0 # начало промежутка
cp = 2*round(pi, 1) # конец промежутка
step = 0.1 # шаг перебора x при отрисовке

root = Tk()

canv = Canvas(height=ch, width=cw, bg='snow')
canv.pack()

cx, cy = cell_w * 1, ch // 2 # координаты центра

# сетка + засечки на оси x
for x in range(cell_w, cw, cell_w):
	canv.create_line((x,0), (x,ch), fill='grey70', dash=1)
	canv.create_line((x, cy-2), (x, cy+2), fill='black')
# сетка + засечки на оси y
for y in range(cell_h, ch, cell_h):
	canv.create_line((0,y), (cw,y), fill='grey70', dash=1)
	canv.create_line((cx-2, y), (cx+2, y), fill='black')
 
canv.create_line((0, cy), (cw, cy)) # ось x
canv.create_line((cx+cp*cell_w,0), (cx+cp*cell_w, ch)) # конец промежутка
canv.create_line((cx, 0), (cx, ch)) # ось y

# кортежи из точек по функциям
f1 = function('sin(sqrt(2*x)) + cos(x)')
f2 = function('sin(x) + cos(2*x)')
f3 = tuple(map(lambda f1, f2: (f1[0], f1[1]*2 - f2[1]*3), f1, f2))

# отрисовка функций
canv.create_line(tuple(map(center, f1)), fill='red')
canv.create_line(tuple(map(center, f2)), fill='green')
canv.create_line(tuple(map(center, f3)), fill='blue')

root.mainloop()
