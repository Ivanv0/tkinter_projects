from tkinter import Tk,  Canvas
from math import pi, sin, cos

def end_xy(line_length, angle):
	x = center_x + line_length * cos(angle)
	y = center_y + line_length * sin(angle)
	return (x,y)

def animation(event):
	anim = True
	while anim:
		big = canv.create_line((center_x, center_y), end_xy(len_of_big, angle_of_big))
		small = canv.create_line((center_x, center_y), end_xy(len_of_small, angle_of_small))
		canv.update()
		root.after(10)
		angle_of_big += angle_step
		angle_of_small += angle_step / 12
		canv.delete(big)
		canv.delete(small)

root = Tk()

# высота и ширина холста могут быть разными
# это будет выгдядеть странно, но это работает
height = 400
width = 400
upd_time = 10 # время в миллисекундах используемое для анимации

canv = Canvas(root, height=height+10, width=width+10)
canv.pack()
canv.update()

canv.create_oval((5,5), (width+5, height+5))

center_x = (canv.winfo_width() - 4) // 2
center_y = (canv.winfo_height() - 4) // 2

angle_of_big = 0
len_of_big = (canv.winfo_width() - 4) // 2 - 10

angle_of_small = 0
len_of_small = (canv.winfo_width() - 4) // 6

angle_step = pi / 180

while True:
	big = canv.create_line((center_x, center_y), end_xy(len_of_big, angle_of_big))
	small = canv.create_line((center_x, center_y), end_xy(len_of_small, angle_of_small))
	canv.update()
	root.after(upd_time)
	angle_of_big += angle_step
	angle_of_small += angle_step / 12
	canv.delete(big)
	canv.delete(small)

root.mainloop()
# при закрытии выдаёт ошибку связанную с прерыванием
# стрелки кажется не синхронизированы из-за округления