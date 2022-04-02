from tkinter import Tk, Canvas
from math import pi, sqrt, sin, cos

def center(dot):
	x, y = dot
	x *= cell_w
	x += cx
	y *= cell_h
	y = cy - y
	return (x, y)

def function(f):
	sp = []
	x = np
	while x < cp:
		sp.append((x, eval(f)))
		x += step
	return tuple(sp)

cell_h = 40
cell_w = 100
ch = cell_h * 14
cw = cell_w * 8
np = 0
cp = 2*round(pi, 1)
step = 0.1

root = Tk()

canv = Canvas(height=ch, width=cw, bg='snow')
canv.pack()

cx, cy = cell_w * 1, ch // 2

for x in range(cell_w, cw, cell_w):
	canv.create_line((x,0), (x,ch), fill='grey70', dash=1)
	canv.create_line((x, cy-2), (x, cy+2), fill='black')
for y in range(cell_h, ch, cell_h):
	canv.create_line((0,y), (cw,y), fill='grey70', dash=1)
	canv.create_line((cx-2, y), (cx+2, y), fill='black')
 
canv.create_line((0, cy), (cw, cy))
canv.create_line((cx, 0), (cx, ch))

f1 = function('sin(sqrt(2*x)) + cos(x)')
f2 = function('sin(x) + cos(2*x)')
f3 = tuple(map(lambda x, y: (x[0], x[1]*2 - y[1]*3), f1, f2))

canv.create_line(tuple(map(center, f1)), fill='red')
canv.create_line(tuple(map(center, f2)), fill='green')
canv.create_line(tuple(map(center, f3)), fill='blue')

root.mainloop()
